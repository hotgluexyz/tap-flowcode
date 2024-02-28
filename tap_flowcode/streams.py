"""Stream type classes for tap-flowcode."""

from typing import Any, Optional

from singer_sdk import typing as th

from tap_flowcode.client import FlowcodeStream
from pendulum import parse

class UsersStream(FlowcodeStream):
    """Define custom stream."""
    name = "users"
    path = "/ListContacts"
    records_jsonpath = "$.conversions[*]"
    replication_key = "lastConvertedAt"
    rest_method = "POST"

    schema = th.PropertiesList(
        th.Property("email", th.StringType),
        th.Property("name", th.StringType),
        th.Property("phone", th.StringType),
        th.Property("lastConvertedAt", th.DateTimeType),
    ).to_dict()

    def get_starting_time(self, context):
        start_date = self.config.get("start_date")
        base_date = parse("2024-02-01T00:00:00Z")
        if start_date:
            start_date = parse(self.config.get("start_date")) 
            if start_date < base_date:
                start_date = base_date
        rep_key = self.get_starting_timestamp(context)
        return rep_key or start_date

    def prepare_request_payload(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Optional[dict]:
        payload = {
            "orgId":self.config.get("org_id"),
            "workspaceId":self.config.get("workspace_id"),
        }
        
        start_date = self.get_starting_time(context)
        if start_date:
            start_date = start_date.strftime('%Y-%m-%dT%H:%M:%SZ')
            payload["filter"] = {
                "date_filter": {
                    "timezone": "Etc/UCT",
                    "start_time": start_date
                }
            }
        return payload
    
    def post_process(self, row: dict, context: dict) -> dict :
        new_row = {}
        new_row["lastConvertedAt"] = row["lastConvertedAt"]
        new_row.update(row["user"])
        return new_row
    