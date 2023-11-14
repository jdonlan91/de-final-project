from src.loader.utils.seed_dim_date import seed_dim_date
from unittest.mock import patch, MagicMock


@patch("src.loader.utils.seed_dim_date.create_connection")
def test_runs_correct_sql_query(mock_create_connection):
    mock_conn = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.run.return_value = []

    seed_dim_date(None)
    print(mock_conn.run.mock_calls[0])
    mock_conn.run.assert_any_call(
        """INSERT INTO dim_date
(date_id, year, month, day, day_of_week, day_name, month_name, quarter)
VALUES ('2022-01-01', 2022, 1,
1, 6, 'Saturday',
'January', 1);""")


@patch("src.loader.utils.seed_dim_date.create_connection")
def test_runs_query_for_every_date_in_2022_to_2024(mock_create_connection):
    mock_conn = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.run.return_value = []

    seed_dim_date(None)

    assert mock_conn.run.call_count == 1096
