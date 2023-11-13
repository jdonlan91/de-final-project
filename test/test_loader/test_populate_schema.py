import pytest
from unittest.mock import patch, MagicMock

from src.loader.utils.populate_schema import populate_schema


@pytest.fixture
def test_design_data():
    return """design_id,design_name,file_location,file_name
8,Wooden,/usr,wooden-20220717-npgz.json
9,Test,/usr,test-20220718-abcd.json"""


@pytest.fixture
def test_clms():
    return "design_id,design_name,file_location,file_name"


@pytest.fixture
def test_conflict():
    conflict = "design_name = EXCLUDED.design_name, "
    conflict += "file_location = EXCLUDED.file_location, "
    conflict += "file_name = EXCLUDED.file_name"
    return conflict


@pytest.fixture
def test_db_credentials():
    return {
        "DB_USERNAME": "test_username",
        "DB_NAME": "test_name",
        "DB_HOST": "test_host",
        "DB_PASSWORD": "test_password"
    }


@patch("src.loader.utils.populate_schema.create_connection")
@patch("src.loader.utils.populate_schema.StringIO")
def test_runs_correct_query_for_design_table(
    mock_stream,
    mock_create_connection,
    test_db_credentials,
    test_design_data,
    test_clms,
    test_conflict
):

    mock_conn = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.run.return_value = []
    mock_stream.return_value = "test_object"

    populate_schema(test_db_credentials, "dim_design", test_design_data)

    mock_conn.run.assert_any_call("BEGIN;")
    mock_conn.run.assert_any_call("""CREATE TEMP TABLE temp_dim_design
 (LIKE dim_design) ON COMMIT DROP;""")
    mock_conn.run.assert_any_call(f"""COPY temp_dim_design ({test_clms})
 FROM STDIN WITH CSV HEADER;""", stream="test_object")
    mock_conn.run.assert_any_call(f"""INSERT INTO dim_design ({test_clms})
 SELECT * FROM temp_dim_design
 ON CONFLICT (design_id) DO UPDATE SET {test_conflict};""")
    mock_conn.run.assert_any_call("COMMIT;")


def test_raises_an_exception(test_db_credentials, test_design_data):
    with pytest.raises(Exception):
        populate_schema(test_db_credentials, "dim_design", test_design_data)
