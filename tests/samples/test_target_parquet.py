"""Test class creation."""

import shutil
import uuid
from pathlib import Path

import pytest

from samples.sample_target_parquet.parquet_target import SampleTargetParquet
from singer_sdk.testing import TargetTestRunner, get_test_class
from singer_sdk.testing.suites import target_tests

SAMPLE_FILEPATH = Path(f".output/test_{uuid.uuid4()}/")
SAMPLE_FILENAME = SAMPLE_FILEPATH / "testfile.parquet"
SAMPLE_CONFIG = {"filepath": str(SAMPLE_FILENAME)}

StandardTestsTargetCSV = get_test_class(
    test_runner=TargetTestRunner(
        target_class=SampleTargetParquet, config=SAMPLE_CONFIG
    ),
    test_suites=[target_tests],
)


@pytest.mark.skipif("sys.version_info >= (3,11)")
class TestTargetCSV(StandardTestsTargetCSV):
    """Standard Target Tests."""

    @pytest.fixture(scope="class")
    def test_output_dir(self):
        return SAMPLE_FILEPATH

    @pytest.fixture(scope="class")
    def resource(self, test_output_dir):
        test_output_dir.mkdir(parents=True, exist_ok=True)
        yield test_output_dir
        shutil.rmtree(test_output_dir)