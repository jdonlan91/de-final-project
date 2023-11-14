from pg8000.native import Connection, identifier
from io import StringIO


def create_connection(db_credentials):
    return Connection(
        user=db_credentials["DB_USERNAME"],
        password=db_credentials["DB_PASSWORD"],
        host=db_credentials["DB_HOST"],
        database=db_credentials["DB_NAME"],
    )


def populate_schema(db_credentials, file_name, csv_string):
    """
    Takes data in csv format from read_parquet and populates
    a star schema database with this data.

    Args:
        csv string: string from read_parquet.

    Returns:

    Raises:
        Exception when error connecting to database.

    """
    try:
        conn = create_connection(db_credentials)
        table_name = file_name.split('/')[0]

        temp_tbl_name = f"temp_{table_name}"
        column_names = csv_string.split("\n")[0]
        column_names_array = column_names.split(",")

        create_temp_tbl = f"""CREATE TEMP TABLE {identifier(temp_tbl_name)}
 (LIKE {table_name}) ON COMMIT DROP;"""

        populate_temp = f"""COPY {identifier(temp_tbl_name)} ({column_names})
 FROM STDIN WITH CSV HEADER;"""

        query = f"""INSERT INTO {identifier(table_name)} ({column_names})
 SELECT * FROM {identifier(temp_tbl_name)}
 ON CONFLICT ({identifier(column_names_array[0])}) DO UPDATE SET"""

        for column in column_names_array:
            logic = f" {identifier(column)} = EXCLUDED.{identifier(column)},"
            if column != column_names_array[0]:
                query += logic

        formatted_query = f"{query[:-1]};"

        csv_obj = StringIO(csv_string)

        conn.run("BEGIN;")
        conn.run(create_temp_tbl)
        conn.run(populate_temp, stream=csv_obj)
        conn.run(formatted_query)
        conn.run("COMMIT;")
        return f"File {file_name} loaded."

    except Exception as e:
        raise e
