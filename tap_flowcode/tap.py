"""Flowcode tap class."""

from typing import List

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  
from tap_flowcode.streams import (
    UsersStream,
)

STREAM_TYPES = [
    UsersStream,
]


class TapFlowcode(Tap):
    """Flowcode tap class."""
    name = "tap-flowcode"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "api_key",
            th.StringType,
            required=True,
        ),
        th.Property(
            "base_url",
            th.StringType,
        ),
        th.Property(
            "org_id",
            th.StringType,
            required=True,
        ),
        th.Property(
            "workspace_id",
            th.StringType,
            required=True,
        ),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]
    
if __name__ == "__main__":
    TapFlowcode.cli()
