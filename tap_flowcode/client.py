"""REST client handling, including FlowcodeStream base class."""

from pathlib import Path
from typing import Any, Optional

import requests
from pendulum import parse
from singer_sdk.authenticators import APIKeyAuthenticator
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream

from tap_flowcode.auth import OAuth2Authenticator

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class FlowcodeStream(RESTStream):
    """Flowcode stream class."""

    url_base = "https://conversions.stg.flowcode.com/abacus.v1.AbacusService"
    records_jsonpath = "$[*]"
    next_page_token_jsonpath = "$.pageInfo.endCursor"

    @property
    def authenticator(self):
        """Return a new authenticator object."""
        if self.config.get("client_id"):
            oauth_url = "https://auth-stg.flowcode.com/oauth/token"
            return OAuth2Authenticator(self, self.config, auth_endpoint=oauth_url)
        return APIKeyAuthenticator.create_for_stream(
            self, key="apikey", value=self.config.get("api_key"), location="header"
        )

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        headers = {}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        return headers

    def get_next_page_token(
        self, response: requests.Response, previous_token: Optional[Any]
    ) -> Optional[Any]:
        """Return a token for identifying next page or None if no more pages."""
        if self.next_page_token_jsonpath:
            all_matches = extract_jsonpath(
                self.next_page_token_jsonpath, response.json()
            )
            first_match = next(iter(all_matches), None)
            next_page_token = first_match
        return next_page_token

    def get_starting_time(self, context):
        start_date = self.config.get("start_date")
        if start_date:
            start_date = parse(self.config.get("start_date"))
        rep_key = self.get_starting_timestamp(context)
        return rep_key or start_date
