import pytest

from unittest.mock import patch, MagicMock
from pg8000.exceptions import InterfaceError

from src.ingestor.utils.fetch_table_names import create_connection, fetch_table_names


class TestCreateConnection:
    def test_create_connection_failure(self):
        db_credentials = {
            "DB_USERNAME": "invalid_user",
            "DB_PASSWORD": "invalid_password",
            "DB_HOST": "invalid_host",
            "DB_NAME": "invalid_db",
        }

        with pytest.raises(InterfaceError):
            create_connection(db_credentials)
            

class TestFetchTableNames:    
    @pytest.fixture(autouse=True)
    def test_db_credentials(self):
        mock_env = {
            "DB_USERNAME": "test_username",
            "DB_NAME": "test_name",
            "DB_HOST": "test_host",
            "DB_PASSWORD": "test_password"
        }

        with patch.dict("os.environ", mock_env, clear=True):
            yield {
                "DB_USERNAME": mock_env["DB_USERNAME"],
                "DB_NAME": mock_env["DB_NAME"],
                "DB_HOST": mock_env["DB_HOST"],
                "DB_PASSWORD": mock_env["DB_PASSWORD"],
            }
    
    def test_returns_a_list(self):
        result = fetch_table_names('test_database')
        assert isinstance(result, list)
        
    def test_returns_an_empty_list(self):
        result = fetch_table_names('empty_database')
        assert result == []
        
    def test_returns_a_list_of_table_names(self):
        result = fetch_table_names('test_database')
        expected = ['table_one', 'table_two', 'table_three']
        assert result == expected
        
    def test_raises_an_exception(self):
        result = fetch_table_names('invalid_database')
        with pytest.raises(Exception):
            result
            
            
