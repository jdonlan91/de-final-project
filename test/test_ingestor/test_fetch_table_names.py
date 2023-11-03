import pytest

from src.ingestor.utils.fetch_table_names import fetch_table_names

class TestFetchTableNames:
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
