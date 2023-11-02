from pg8000.native import Connection, identifier, literal
from datetime import datetime


def create_connection(db_credentials):
    return Connection(
        user=db_credentials["DB_USERNAME"],
        password=db_credentials["DB_PASSWORD"],
        host=db_credentials["DB_HOST"],
        database=db_credentials["DB_NAME"],
    )


def run_query(db_connection, query):
    return db_connection.run(query)


def convert_lists_to_dicts(list_of_lists, column_names):
    list_of_dicts = []

    for row in list_of_lists:
        row_as_dict = {
            column_names[i]: cell.isoformat(sep=" ", timespec="milliseconds")
            if type(cell) is datetime
            else cell for i,
            cell in enumerate(row)
        }
        list_of_dicts.append(row_as_dict)

    return list_of_dicts


def fetch_new_data(table_name: str, timestamp, db_credentials) -> list[dict]:
    """Fetches data more recent than the timestamp from a specified table
    and returns the rows as a list of dictionaries

    Args:
        table_name <string>: The table name
        timestamp <datetime object>: timestamp from which data will be selected
        db_credentials <dictionary>: credentials for accessing the database.
        Credentials needs to be in the following format:
            {
                "DB_USERNAME": ...
                "DB_NAME": ...
                "DB_HOST": ...
                "DB_PASSWORD": ...
            }

    Returns:
        returns <list[dict]> representing the relevant rows of the database
    """
    try:
        conn = create_connection(db_credentials)

        query = f"""
            SELECT * FROM {identifier(table_name)}
            WHERE last_updated > {literal(timestamp)}
        """
        results_list_of_lists = run_query(conn, query)
        column_names = [column["name"] for column in conn.columns]

        return convert_lists_to_dicts(results_list_of_lists, column_names)

    except Exception as e:
        raise e
