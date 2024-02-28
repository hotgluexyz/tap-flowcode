"""Flowcode tap class."""

from typing import List

from singer_sdk import Stream, Tap
from singer_sdk import typing as th

from tap_flowcode.streams import UsersStream

STREAM_TYPES = [
    UsersStream,
]


class TapFlowcode(Tap):
    """Flowcode tap class."""

    name = "tap-flowcode"

    def __init__(
        self,
        config=None,
        catalog=None,
        state=None,
        parse_env_config=False,
        validate_config=True,
    ) -> None:
        self.config_file = config[0]
        super().__init__(config, catalog, state, parse_env_config, validate_config)

    config_jsonschema = th.PropertiesList(
        th.Property(
            "api_key",
            th.StringType,
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
        th.Property(
            "client_id",
            th.StringType,
        ),
        th.Property(
            "client_secret",
            th.StringType,
        ),
        th.Property(
            "refresh_token", 
            th.StringType
        ),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]


if __name__ == "__main__":
    TapFlowcode.cli()
