import pyarrow

from src.processor.utils.convert_to_parquet import convert_to_parquet


def test_returns_pyarrow_table():
    input = [{"staff_id": 1, "first_name": "Jeremie"}]
    assert isinstance(convert_to_parquet(input), pyarrow.Table)


def test_returns_empty_table_when_empty_list_passed():

    output = convert_to_parquet([])
    assert output.num_columns == 0
    assert output.num_rows == 0


def test_returns_correct_columns_and_rows_when_list_of_one_dict_passed():
    input = [{"staff_id": 1, "first_name": "Jeremie"}]
    output = convert_to_parquet(input)

    assert output.num_columns == 2
    assert output.num_rows == 1
    assert output.column_names == ["staff_id", "first_name"]


def test_returns_correct_columns_and_rows_when_list_of_multi_dicts_passed():
    input = [
        {"staff_id": 1, "first_name": "Jeremie"},
        {"staff_id": 2, "first_name": "Peter"},
        {"staff_id": 3, "first_name": "Steve"},
        {"staff_id": 4, "first_name": "Mary"},
    ]
    output = convert_to_parquet(input)

    assert output.num_columns == 2
    assert output.num_rows == 4
    assert output.column_names == ["staff_id", "first_name"]
