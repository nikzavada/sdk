"""Default JSON Schema to support config for built-in capabilities."""

from __future__ import annotations

from singer_sdk.typing import (
    ArrayType,
    BooleanType,
    IntegerType,
    NumberType,
    ObjectType,
    OneOf,
    PropertiesList,
    Property,
    StringType,
)

from ._enum import TargetLoadMethods

STREAM_MAPS_CONFIG = PropertiesList(
    Property(
        "stream_maps",
        ObjectType(),
        description=(
            "Config object for stream maps capability. "
            "For more information check out "
            "[Stream Maps](https://sdk.meltano.com/en/latest/stream_maps.html)."
        ),
    ),
    Property(
        "stream_map_config",
        ObjectType(),
        description="User-defined config values to be used within map expressions.",
    ),
    Property(
        "faker_config",
        ObjectType(
            Property(
                "seed",
                OneOf(NumberType, StringType, BooleanType),
                description=(
                    "Value to seed the Faker generator for deterministic output: "
                    "https://faker.readthedocs.io/en/master/#seeding-the-generator"
                ),
            ),
            Property(
                "locale",
                OneOf(StringType, ArrayType(StringType)),
                description=(
                    "One or more LCID locale strings to produce localized output for: "
                    "https://faker.readthedocs.io/en/master/#localization"
                ),
            ),
        ),
        description=(
            "Config for the [`Faker`](https://faker.readthedocs.io/en/master/) "
            "instance variable `fake` used within map expressions. Only applicable if "
            "the plugin specifies `faker` as an additional dependency (through the "
            "`singer-sdk` `faker` extra or directly)."
        ),
    ),
).to_dict()

FLATTENING_CONFIG = PropertiesList(
    Property(
        "flattening_enabled",
        BooleanType(),
        description=(
            "'True' to enable schema flattening and automatically expand nested "
            "properties."
        ),
    ),
    Property(
        "flattening_max_depth",
        IntegerType(),
        description="The max depth to flatten schemas.",
    ),
).to_dict()

BATCH_CONFIG = PropertiesList(
    Property(
        "batch_config",
        description="",
        wrapped=ObjectType(
            Property(
                "encoding",
                description="Specifies the format and compression of the batch files.",
                wrapped=ObjectType(
                    Property(
                        "format",
                        StringType,
                        allowed_values=["jsonl", "parquet"],
                        description="Format to use for batch files.",
                    ),
                    Property(
                        "compression",
                        StringType,
                        allowed_values=["gzip", "none"],
                        description="Compression format to use for batch files.",
                    ),
                ),
            ),
            Property(
                "storage",
                description="Defines the storage layer to use when writing batch files",
                wrapped=ObjectType(
                    Property(
                        "root",
                        StringType,
                        description="Root path to use when writing batch files.",
                    ),
                    Property(
                        "prefix",
                        StringType,
                        description="Prefix to use when writing batch files.",
                    ),
                ),
            ),
        ),
    ),
).to_dict()

TARGET_SCHEMA_CONFIG = PropertiesList(
    Property(
        "default_target_schema",
        StringType(),
        description="The default target database schema name to use for all streams.",
    ),
).to_dict()

ADD_RECORD_METADATA_CONFIG = PropertiesList(
    Property(
        "add_record_metadata",
        BooleanType(),
        description="Add metadata to records.",
    ),
).to_dict()

TARGET_HARD_DELETE_CONFIG = PropertiesList(
    Property(
        "hard_delete",
        BooleanType(),
        description="Hard delete records.",
        default=False,
    ),
).to_dict()

TARGET_VALIDATE_RECORDS_CONFIG = PropertiesList(
    Property(
        "validate_records",
        BooleanType(),
        description="Whether to validate the schema of the incoming streams.",
        default=True,
    ),
).to_dict()

TARGET_BATCH_SIZE_ROWS_CONFIG = PropertiesList(
    Property(
        "batch_size_rows",
        IntegerType,
        description="Maximum number of rows in each batch.",
    ),
).to_dict()

TARGET_LOAD_METHOD_CONFIG = PropertiesList(
    Property(
        "load_method",
        StringType(),
        description=(
            "The method to use when loading data into the destination. "
            "`append-only` will always write all input records whether that records "
            "already exists or not. `upsert` will update existing records and insert "
            "new records. `overwrite` will delete all existing records and insert all "
            "input records."
        ),
        allowed_values=[
            TargetLoadMethods.APPEND_ONLY,
            TargetLoadMethods.UPSERT,
            TargetLoadMethods.OVERWRITE,
        ],
        default=TargetLoadMethods.APPEND_ONLY,
    ),
).to_dict()
