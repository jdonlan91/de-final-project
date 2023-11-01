import os
import pytest
import boto3
from moto import mock_s3
from src.ingester.dump_data import dump_data


@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""

    os.environ["AWS_ACCESS_KEY_ID"] = "test"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
    os.environ["AWS_SECURITY_TOKEN"] = "test"
    os.environ["AWS_SESSION_TOKEN"] = "test"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


@pytest.fixture(scope="function")
def s3(aws_credentials):
    with mock_s3():
        yield boto3.client("s3", region_name="eu-west-2")


@pytest.fixture
def empty_bucket(s3):
    s3.create_bucket(
        Bucket="test_ingested_bucket",
        CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
    )


@pytest.fixture
def test_csv():
    return """
        seq,name/first,name/last,age,street,city,state,zip,dollar,pick,date
        1,Curtis,Ruiz,54,Relgo Way,Zappeguk,MN,25633,$4978.53,WHITE,10/30/1941
        2,Jon,Haynes,54,Jozif Terrace,Zegzavid,ND,41182,$754.87,BLUE,06/12/2048
    """


class TestDumpData:
    def test_returns_a_string(self, test_csv, empty_bucket):
        assert (
            dump_data(
                "test_table",
                "31-10-23-152600",
                test_csv,
                "test_ingested_bucket"
            ) == "Data dumped successfully!"
        )

    def test_puts_csv_file_in_bucket(self, s3, test_csv, empty_bucket):
        dump_data("test_table", "31-10-23-152600",
                  test_csv, "test_ingested_bucket")
        response = s3.list_objects(Bucket="test_ingested_bucket")
        filename = response["Contents"][0]["Key"]
        assert filename == "test_table-31-10-23-152600.csv"

    def test_raises_an_error(self, test_csv):
        with pytest.raises(Exception):
            dump_data('test_table', '31-10-152600',
                      test_csv, "invalid-bucket-011123")
