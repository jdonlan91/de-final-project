from dotenv import load_dotenv
from src.ingester.fetch_new_data import fetch_new_data
import pytest
from dotenv import load_dotenv
from os import environ

# load_dotenv()
# db_credentials = {
#     "DB_USERNAME": environ["DB_USERNAME"],
#     "DB_NAME": environ["DB_NAME"],
#     "DB_HOST": environ["DB_HOST"],
#     "DB_PASSWORD": environ["DB_PASSWORD"]
# }


@pytest.fixture
def db_credentials():
    load_dotenv()
    return {
        "DB_USERNAME": environ["DB_USERNAME"],
        "DB_NAME": environ["DB_NAME"],
        "DB_HOST": environ["DB_HOST"],
        "DB_PASSWORD": environ["DB_PASSWORD"]
    }


def test_example(db_credentials):
    fetch_new_data('test_table', db_credentials)
    print()
    assert False
