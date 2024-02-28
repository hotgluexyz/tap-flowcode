"""Stream type classes for tap-flowcode."""

from typing import Any, Optional

from singer_sdk import typing as th

from tap_flowcode.client import FlowcodeStream


class UsersStream(FlowcodeStream):
    """Define custom stream."""

    name = "users"
    path = "/ListContacts"
    records_jsonpath = "$.conversions[*]"
    replication_key = "firstConvertedAt"
    rest_method = "POST"

    schema = th.PropertiesList(
        th.Property("email", th.StringType),
        th.Property("name", th.StringType),
        th.Property("phone", th.StringType),
        th.Property("firstConvertedAt", th.DateTimeType),
    ).to_dict()

    def prepare_request_payload(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Optional[dict]:
        payload = {
            "orgId": self.config.get("org_id"),
            "workspaceId": self.config.get("workspace_id"),
        }

        start_date = self.get_starting_time(context)
        if start_date:
            start_date = start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
            payload["filter"] = {
                "date_filter": {
                    "timezone": self.config.get("timezone", "Etc/UCT"),
                    "start_time": start_date,
                }
            }
        payload["pagination"] = {
            "order": "ORDER_ASC",
            "orderBy": "name",
        }

        if next_page_token:
            payload["pagination"]["after"] = next_page_token
        return payload

    def post_process(self, row: dict, context: dict) -> dict:
        new_row = {}
        new_row["firstConvertedAt"] = row["firstConvertedAt"]
        new_row.update(row["user"])
        return new_row
