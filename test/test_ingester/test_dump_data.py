from moto import mock_s3
from moto.core import patch_client
import pytest
import os
import boto3
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
        3,Ada,Carlson,61,Cicrer Boulevard,Utetude,ME,21912,$9240.52,YELLOW,11/18/1983
        4,Lester,Reyes,43,Gehru Manor,Ketowar,DE,05912,$9398.47,WHITE,09/01/1955
        5,Lawrence,Estrada,46,Dufcas Lane,Ocfevap,ME,15216,$4241.11,BLUE,05/14/2045
        6,Theresa,Waters,29,Waleh Avenue,Hiwjidgi,MN,12857,$6287.90,GREEN,08/06/1944
        7,Willie,Ferguson,36,Cignud Center,Lemenodu,DC,26480,$8424.98,BLUE,02/02/1980
        8,Thomas,Rodriquez,36,Mesa Boulevard,Punfizcul,CO,94689,$2930.15,WHITE,02/05/1930
        9,Caleb,Bradley,62,Sepuw Extension,Objojal,NY,70755,$8556.95,GREEN,12/28/2051
        10,Miguel,Green,37,Polca Key,Ramuka,MS,94261,$7878.88,BLUE,12/05/1954
        11,Josie,Vaughn,38,Zugo Terrace,Migejut,WV,74799,$2634.21,WHITE,11/22/1943
        12,Connor,White,25,Ejumuw Pike,Bucagsu,DE,26768,$848.69,YELLOW,02/19/1959
        13,Brian,Newton,18,Nonbep Plaza,Kufloaf,TX,53478,$1895.66,GREEN,04/08/2022
        14,Mina,Higgins,20,Daive Mill,Sepaplif,IA,24221,$6935.14,YELLOW,09/14/1941
        15,Essie,Leonard,39,Cokez Point,Suriweko,WY,94170,$3768.29,GREEN,11/28/1946
        16,Allie,Lowe,29,Nehrik Avenue,Modwiwuj,MN,78389,$6009.16,RED,01/23/2034
    """


class TestDumpData:
    def test_returns_a_string(self, test_csv, empty_bucket):
        assert (
            dump_data("test_table", "31-10-23-152600", test_csv, "test_ingested_bucket")
            == "Data dumped successfully!"
        )

    def test_puts_csv_file_in_bucket(self, s3, test_csv, empty_bucket):
        dump_data("test_table", "31-10-23-152600", test_csv, "test_ingested_bucket")
        response = s3.list_objects(
            Bucket="test_ingested_bucket",
        )
        assert response["Contents"][0]["Key"] == "test_table-31-10-23-152600.csv"


# dumps CSV data into ingestion bucket

# throws an error if passed a filetype that is not CSV
