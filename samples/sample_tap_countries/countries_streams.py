"""Sample tap stream test for tap-countries.

This uses a free "Countries API" which does not require authentication.

See the online explorer and query builder here:
  - https://countries.trevorblades.com/
"""

from __future__ import annotations

import abc
import sys
from typing import Iterable  # noqa: ICN003

from singer_sdk import typing as th
from singer_sdk.streams.graphql import GraphQLStream

if sys.version_info < (3, 9):
    import importlib_resources
else:
    from importlib import resources as importlib_resources


SCHEMAS_DIR = importlib_resources.files(__package__) / "schemas"


class CountriesAPIStream(GraphQLStream, metaclass=abc.ABCMeta):
    """Sample tap test for countries.

    NOTE: This API does not require authentication.
    """

    url_base = "https://countries.trevorblades.com/"


class CountriesStream(CountriesAPIStream):
    """Countries API stream."""

    name = "countries"
    primary_keys = ("code",)
    query = """
        countries {
            code
            name
            native
            phone
            continent {
                code
                name
            }
            capital
            currency
            languages {
                code
                name
            }
            emoji
        }
        """
    schema = th.PropertiesList(
        th.Property("code", th.StringType),
        th.Property("name", th.StringType),
        th.Property("native", th.StringType),
        th.Property("phone", th.StringType),
        th.Property("capital", th.StringType),
        th.Property("currency", th.StringType),
        th.Property("emoji", th.StringType),
        th.Property(
            "continent",
            th.ObjectType(
                th.Property("code", th.StringType),
                th.Property("name", th.StringType),
            ),
        ),
        th.Property(
            "languages",
            th.ArrayType(
                th.ObjectType(
                    th.Property("code", th.StringType),
                    th.Property("name", th.StringType),
                ),
            ),
        ),
    ).to_dict()

    # FIXME: revert these changes before merging
    def request_records(self, context) -> Iterable[dict]:
        import time  # noqa: PLC0415

        time.sleep(60)  # Simulate a slow stream

        return super().request_records(context)


class ContinentsStream(CountriesAPIStream):
    """Continents stream from the Countries API."""

    name = "continents"
    primary_keys = ("code",)
    schema_filepath = SCHEMAS_DIR / "continents.json"
    query = """
        continents {
            code
            name
        }
        """
