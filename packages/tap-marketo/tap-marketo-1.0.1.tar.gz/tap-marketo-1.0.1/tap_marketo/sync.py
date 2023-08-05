import csv
import io
import json
import pendulum
import singer
from tap_marketo.client import ExportFailed
from singer import bookmarks

# We can request up to 30 days worth of activities per export.
MAX_EXPORT_DAYS = 30

BASE_ACTIVITY_FIELDS = [
    "marketoGUID",
    "leadId",
    "activityDate",
    "activityTypeId",
]

ACTIVITY_FIELDS = BASE_ACTIVITY_FIELDS + [
    "primaryAttributeValue",
    "primaryAttributeValueId",
    "attributes",
]

NO_ASSET_MSG = "No assets found for the given search criteria."
NO_CORONA_WARNING = (
    "Your account does not have Corona support enabled. Without Corona, each sync of "
    "the Leads table requires a full export which can lead to lower data freshness. "
    "Please contact Marketo to request Corona support be added to your account."
)


def format_value(value, schema):
    if not isinstance(schema["type"], list):
        field_type = [schema["type"]]
    else:
        field_type = schema["type"]

    if value in [None, "", 'null']:
        return None
    elif schema.get("format") == "date-time":
        return pendulum.parse(value).isoformat()
    elif "integer" in field_type:
        return int(value)
    elif "number" in field_type:
        return float(value)
    elif "boolean" in field_type:
        if isinstance(value, bool):
            return value
        return value.lower() == "true"

    return value


def format_values(stream, row):
    rtn = {}
    for field, schema in stream["schema"]["properties"].items():
        if not schema.get("selected") and not (schema.get("inclusion") == "automatic"):
            continue
        rtn[field] = format_value(row.get(field), schema)
    return rtn


def parse_csv_line(line):
    reader = csv.reader(io.StringIO(line.decode('utf-8')))
    return next(reader)


def flatten_activity(row, schema):
    # Start with the base fields
    rtn = {field: row[field] for field in BASE_ACTIVITY_FIELDS}

    # Move the primary attribute to the named column. Primary attribute
    # has a `field` and a `field_id` entry in the schema, is marked for
    # automatic inclusion, and isn't one of the base activity fields.
    for field, field_schema in schema["properties"].items():
        if field_schema["inclusion"] == "automatic" and field not in ACTIVITY_FIELDS:
            rtn[field] = row["primaryAttributeValue"]

    # Now flatten the attrs json to it's selected columns
    if "attributes" in row:
        attrs = json.loads(row["attributes"])
        for key, value in attrs.items():
            key = key.lower().replace(" ", "_")
            rtn[key] = value

    return rtn

def get_or_create_export_for_leads(client, state, stream, fields, start_date):
    export_id = bookmarks.get_bookmark(state, stream["tap_stream_id"], "export_id")
    export_end = bookmarks.get_bookmark(state, stream["tap_stream_id"], "export_end")

    if export_id is None:
        if client.use_corona:
            query_field = "updatedAt"
        else:
            query_field = "createdAt"
        
        export_end = start_date.add(days=MAX_EXPORT_DAYS)
        if export_end >= pendulum.utcnow():
            export_end = pendulum.utcnow()

        query = {query_field: {"startAt": start_date.isoformat(), "endAt": export_end.isoformat()}}

        # Create the new export and store the id and end date in state.
        # Does not start the export (must POST to the "enqueue" endpoint).
        export_id = client.create_export("leads", fields, query)
        update_state_with_export_info(state, stream, export_id=export_id, export_end=export_end.isoformat())

    else:
        export_end = pendulum.parse(export_end)    

    return export_id, export_end

def write_leads_records(client, stream, lines, og_bookmark_value, record_count):
    headers = parse_csv_line(next(lines))

    for line in lines:
        parsed_line = parse_csv_line(line)
        parsed_line = dict(zip(headers, parsed_line))
        line_updated_at = pendulum.parse(parsed_line["updatedAt"])
        #accounts without corona need to have a manual filter on records
        if client.use_corona or (line_updated_at >= og_bookmark_value):

            record = format_values(stream, parsed_line)
            singer.write_record(stream["tap_stream_id"], record)
            record_count += 1

    return record_count

def sync_leads(client, state, stream):
    # http://developers.marketo.com/rest-api/bulk-extract/bulk-lead-extract/
    singer.write_schema(stream["tap_stream_id"], stream["schema"], stream["key_properties"])
    record_count = 0
    replication_key = stream.get("replication_key")
    tap_stream_id = stream.get("tap_stream_id")
    tap_job_start_time = pendulum.utcnow()
    fields = [f for f, s in stream["schema"]["properties"].items() if s.get("selected")]

    og_bookmark_value = pendulum.parse(bookmarks.get_bookmark(state, tap_stream_id, replication_key))
    bookmark_date = og_bookmark_value

    while bookmark_date < tap_job_start_time:
        export_id, export_end = get_or_create_export_for_leads(client, state, stream, fields, bookmark_date)

        try:
            client.wait_for_export("leads", export_id)
        except ExportFailed as ex:
            update_state_with_export_info(state, stream)
            singer.log_critical("Export job failure.  Status was" + ex)

        lines = client.stream_export("leads", export_id)

        record_count = write_leads_records(client, stream, lines, og_bookmark_value, record_count)

        if client.use_corona:
            state = update_state_with_export_info(state, stream, bookmark=export_end.isoformat(), \
                                          export_id=None, export_end=None)
        else:
            state = update_state_with_export_info(state, stream, \
                                          export_id=None, export_end=None)

        bookmark_date = export_end

    state = update_state_with_export_info(state, stream, bookmark=bookmark_date.isoformat(), \
                                          export_id=None, export_end=None)


    return state, record_count

def get_or_create_export_for_activities(client, state, stream):
    export_id = bookmarks.get_bookmark(state, stream["tap_stream_id"], "export_id")

    if not export_id:
        # Stream names for activities are `activities_X` where X is the
        # activity type id in Marketo. We need the activity type id to
        # build the query.
        _, activity_type_id = stream["tap_stream_id"].split("_")

        # Activities must be queried by `createdAt` even though
        # that is not a real field. `createdAt` proxies `activityDate`.
        # The activity type id must also be included in the query. The
        # largest date range that can be used for activities is 30 days.
        start_date = bookmarks.get_bookmark(state, stream["tap_stream_id"], stream["replication_key"])
        start_pen = pendulum.parse(start_date)
        end_pen = start_pen.add(days=MAX_EXPORT_DAYS)
        if end_pen >= pendulum.utcnow():
            end_pen = pendulum.utcnow()

        end_date = end_pen.isoformat()
        query = {"createdAt": {"startAt": start_date, "endAt": end_date},
                 "activityTypeIds": [activity_type_id]}

        # Create the new export and store the id and end date in state.
        # Does not start the export (must POST to the "enqueue" endpoint).
        export_id = client.create_export("activities", ACTIVITY_FIELDS, query)
        update_state_with_export_info(state, stream, export_id=export_id, export_end=end_date)

    return export_id


def update_state_with_export_info(state, stream, bookmark=None, export_id=None, export_end=None):
    state = bookmarks.write_bookmark(state, stream["tap_stream_id"], "export_id", export_id)
    state = bookmarks.write_bookmark(state, stream["tap_stream_id"], "export_end", export_end)
    if bookmark:
        state = bookmarks.write_bookmark(state, stream["tap_stream_id"], stream["replication_key"], bookmark)

    singer.write_state(state)
    return state

def convert_line(stream, headers, line):
    parsed_line = parse_csv_line(line)
    row = dict(zip(headers, parsed_line))
    row = flatten_activity(row, stream["schema"])
    return format_values(stream, row)


def handle_record(state, stream, record):
    start_date = bookmarks.get_bookmark(state, stream["tap_stream_id"], stream["replication_key"])
    if record[stream["replication_key"]] < start_date:
        return 0

    singer.write_record(stream["tap_stream_id"], record)
    return 1


def wait_for_activity_export(client, state, stream, export_id):
    try:
        client.wait_for_export("activities", export_id)
    except ExportFailed:
        update_state_with_export_info(state, stream)
        raise


def sync_activities(client, state, stream):
    # http://developers.marketo.com/rest-api/bulk-extract/bulk-activity-extract/
    singer.write_schema(stream["tap_stream_id"], stream["schema"], stream["key_properties"])
    start_date = bookmarks.get_bookmark(state, stream["tap_stream_id"], stream["replication_key"])
    start_pen = pendulum.parse(start_date)
    job_started = pendulum.utcnow()
    record_count = 0

    while start_pen < job_started:
        export_id = get_or_create_export_for_activities(client, state, stream)

        # If the export fails while running, clear the export information
        # from state so a new export can be run next sync.
        wait_for_activity_export(client, state, stream, export_id)

        # Stream the rows keeping count of the accepted rows.
        lines = client.stream_export("activities", export_id)
        headers = parse_csv_line(next(lines))
        for line in lines:
            record = convert_line(stream, headers, line)
            record_count += handle_record(state, stream, record)

        # The new start date is the end of the previous export. Update
        # the bookmark to the end date and continue with the next export.

        start_date = bookmarks.get_bookmark(state, stream["tap_stream_id"], "export_end")
        update_state_with_export_info(state, stream, bookmark=start_date)
        start_pen = pendulum.parse(start_date)

    return state, record_count


def sync_programs(client, state, stream):
    # http://developers.marketo.com/rest-api/assets/programs/#by_date_range
    #
    # Programs are queryable via their updatedAt time but require and
    # end date as well. As there is no max time range for the query,
    # query from the bookmark value until current.
    #
    # The Programs endpoint uses offsets with a return limit of 200
    # per page. If requesting past the final program, an error message
    # is returned to indicate that the endpoint has been fully synced.
    singer.write_schema("programs", stream["schema"], stream["key_properties"])
    start_date = bookmarks.get_bookmark(state, "programs", "updatedAt")
    end_date = pendulum.utcnow().isoformat()
    params = {
        "maxReturn": 200,
        "offset": 0,
        "earliestUpdatedAt": start_date,
        "latestUpdatedAt": end_date,
    }
    endpoint = "rest/asset/v1/programs.json"

    record_count = 0
    while True:
        data = client.request("GET", endpoint, endpoint_name="programs", params=params)

        # If the no asset message is in the warnings, we have exhausted
        # the search results and can end the sync.
        if NO_ASSET_MSG in data["warnings"]:
            break

        # Each row just needs the values formatted. If the record is
        # newer than the original start date, stream the record.
        for row in data["result"]:
            record = format_values(stream, row)
            if record["updatedAt"] >= start_date:
                record_count += 1
                singer.write_record("programs", record)

        # Increment the offset by the return limit for the next query.
        params["offset"] += params["maxReturn"]

    # Now that we've finished every page we can update the bookmark to
    # the end of the query.
    state = bookmarks.write_bookmark(state, "programs", "updatedAt", end_date)
    singer.write_state(state)
    return state, record_count


def sync_paginated(client, state, stream):
    # http://developers.marketo.com/rest-api/endpoint-reference/lead-database-endpoint-reference/#!/Campaigns/getCampaignsUsingGET
    # http://developers.marketo.com/rest-api/endpoint-reference/lead-database-endpoint-reference/#!/Static_Lists/getListsUsingGET
    #
    # Campaigns and Static Lists are paginated with a max return of 300
    # items per page. There are no filters that can be used to only
    # return updated records.
    singer.write_schema(stream["tap_stream_id"], stream["schema"], stream["key_properties"])
    start_date = bookmarks.get_bookmark(state, stream["tap_stream_id"], stream["replication_key"])
    params = {"batchSize": 300}
    endpoint = "rest/v1/{}.json".format(stream["tap_stream_id"])

    # Paginated requests use paging tokens for retrieving the next page
    # of results. These tokens are stored in the state for resuming
    # syncs. If a paging token exists in state, use it.
    next_page_token = bookmarks.get_bookmark(state, stream["tap_stream_id"], "next_page_token")
    if next_page_token:
        params["nextPageToken"] = next_page_token

    # Keep querying pages of data until no next page token.
    record_count = 0
    job_started = pendulum.utcnow().isoformat()
    while True:
        data = client.request("GET", endpoint, endpoint_name=stream["tap_stream_id"], params=params)

        # Each row just needs the values formatted. If the record is
        # newer than the original start date, stream the record. Finally,
        # update the bookmark if newer than the existing bookmark.
        for row in data["result"]:
            record = format_values(stream, row)
            if record[stream["replication_key"]] >= start_date:
                record_count += 1
                singer.write_record(stream["tap_stream_id"], record)

        # No next page, results are exhausted.
        if "nextPageToken" not in data:
            break

        # Store the next page token in state and continue.
        params["nextPageToken"] = data["nextPageToken"]
        state = bookmarks.write_bookmark(state, stream["tap_stream_id"], "next_page_token", data["nextPageToken"])
        singer.write_state(state)

    # Once all results are exhausted, unset the next page token bookmark
    # so the subsequent sync starts from the beginning.
    state = bookmarks.write_bookmark(state, stream["tap_stream_id"], "next_page_token", None)
    state = bookmarks.write_bookmark(state, stream["tap_stream_id"], stream["replication_key"], job_started)
    singer.write_state(state)
    return state, record_count


def sync_activity_types(client, state, stream):
    # http://developers.marketo.com/rest-api/lead-database/activities/#describe
    #
    # Activity types aren't even paginated. Grab all the results in one
    # request, format the values, and output them.
    singer.write_schema("activity_types", stream["schema"], stream["key_properties"])
    endpoint = "rest/v1/activities/types.json"
    data = client.request("GET", endpoint, endpoint_name="activity_types")
    record_count = 0
    for row in data["result"]:
        record = format_values(stream, row)
        record_count += 1
        singer.write_record("activity_types", record)

    return state, record_count


def sync(client, catalog, state):
    starting_stream = bookmarks.get_currently_syncing(state)
    if starting_stream:
        singer.log_info("Resuming sync from %s", starting_stream)
    else:
        singer.log_info("Starting sync")

    for stream in catalog["streams"]:
        # Skip unselected streams.
        if not stream["schema"].get("selected"):
            singer.log_info("%s: not selected", stream["tap_stream_id"])
            continue

        # Skip streams that have already be synced when resuming.
        if starting_stream and stream["tap_stream_id"] != starting_stream:
            singer.log_info("%s: already synced", stream["tap_stream_id"])
            continue

        singer.log_info("%s: starting sync", stream["tap_stream_id"])

        # Now that we've started, there's no more "starting stream". Set
        # the current stream to resume on next run.
        starting_stream = None
        state = bookmarks.set_currently_syncing(state, stream["tap_stream_id"])
        singer.write_state(state)

        # Sync stream based on type.
        if stream["tap_stream_id"] == "activity_types":
            state, record_count = sync_activity_types(client, state, stream)
        elif stream["tap_stream_id"] == "leads":
            state, record_count = sync_leads(client, state, stream)
        elif stream["tap_stream_id"].startswith("activities_"):
            state, record_count = sync_activities(client, state, stream)
        elif stream["tap_stream_id"] in ["campaigns", "lists"]:
            state, record_count = sync_paginated(client, state, stream)
        elif stream["tap_stream_id"] == "programs":
            state, record_count = sync_programs(client, state, stream)
        else:
            raise Exception("Stream %s not implemented" % stream["tap_stream_id"])

        # Emit metric for record count.
        counter = singer.metrics.record_counter(stream["tap_stream_id"])
        counter.value = record_count
        counter._pop()  # pylint: disable=protected-access

        # Unset current stream.
        state = bookmarks.set_currently_syncing(state, None)
        singer.write_state(state)
        singer.log_info("%s: finished sync", stream["tap_stream_id"])

    singer.log_info("Finished sync")

    # If Corona is not supported, log a warning near the end of the tap
    # log with instructions on how to get Corona supported.
    if not client.use_corona:
        singer.log_warning(NO_CORONA_WARNING)
