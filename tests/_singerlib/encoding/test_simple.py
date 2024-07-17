"""Test IO operations for simple Singer reader and writer."""  # noqa: INP001

from __future__ import annotations

import decimal
import io
from contextlib import nullcontext, redirect_stdout
from textwrap import dedent

import pytest

from singer_sdk._singerlib import RecordMessage
from singer_sdk._singerlib.encoding._simple import SingerReader, SingerWriter
from singer_sdk._singerlib.exceptions import InvalidInputLine


class DummyReader(SingerReader):
    def _process_activate_version_message(self, message_dict: dict) -> None:
        pass

    def _process_batch_message(self, message_dict: dict) -> None:
        pass

    def _process_record_message(self, message_dict: dict) -> None:
        pass

    def _process_schema_message(self, message_dict: dict) -> None:
        pass

    def _process_state_message(self, message_dict: dict) -> None:
        pass


@pytest.mark.parametrize(
    "line,expected,exception",
    [
        pytest.param(
            "not-valid-json",
            None,
            pytest.raises(InvalidInputLine),
            id="unparsable",
        ),
        pytest.param(
            '{"type": "RECORD", "stream": "users", "record": {"id": 1, "value": 1.23}}',
            {
                "type": "RECORD",
                "stream": "users",
                "record": {"id": 1, "value": decimal.Decimal("1.23")},
            },
            nullcontext(),
            id="record",
        ),
    ],
)
def test_deserialize(line, expected, exception):
    reader = DummyReader()
    with exception:
        assert reader.deserialize_json(line) == expected


def test_listen():
    reader = DummyReader()
    input_lines = io.StringIO(
        dedent("""\
        {"type": "SCHEMA", "stream": "users", "schema": {"type": "object", "properties": {"id": {"type": "integer"}, "value": {"type": "number"}}}}
        {"type": "RECORD", "stream": "users", "record": {"id": 1, "value": 1.23}}
        {"type": "RECORD", "stream": "users", "record": {"id": 2, "value": 2.34}}
        {"type": "STATE", "value": {"bookmarks": {"users": {"id": 2}}}}
        {"type": "SCHEMA", "stream": "batches", "schema": {"type": "object", "properties": {"id": {"type": "integer"}, "value": {"type": "number"}}}}
        {"type": "BATCH", "stream": "batches", "encoding": {"format": "jsonl", "compression": "gzip"}, "manifest": ["file1.jsonl.gz", "file2.jsonl.gz"]}
        {"type": "STATE", "value": {"bookmarks": {"users": {"id": 2}, "batches": {"id": 1000000}}}}
    """)  # noqa: E501
    )
    reader.listen(input_lines)


def test_listen_unknown_message():
    reader = DummyReader()
    input_lines = io.StringIO('{"type": "UNKNOWN"}\n')
    with pytest.raises(ValueError, match="Unknown message type"):
        reader.listen(input_lines)


def test_write_message():
    writer = SingerWriter()
    message = RecordMessage(
        stream="test",
        record={"id": 1, "name": "test"},
    )
    with redirect_stdout(io.StringIO()) as out:
        writer.write_message(message)

    assert out.getvalue() == (
        '{"type":"RECORD","stream":"test","record":{"id":1,"name":"test"}}\n'
    )