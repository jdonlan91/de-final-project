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

        column_names_array = csv_string.split("\n")[0].split(",")
        column_names = ",".join(list(map(
            lambda x: identifier(x), column_names_array)))
        csv_obj = StringIO(csv_string)

        """Logic for the fact tables:"""

        if table_name[:4] == "fact":
            query = f"""COPY {identifier(table_name)} ({column_names})
 FROM STDIN WITH CSV HEADER;"""
            conn.run(query, stream=csv_obj)
            return f"File {file_name} loaded."

        """Logic for the dim tables:"""

        temp_tbl_name = f"temp_{table_name}"

        create_temp_tb = f"""CREATE TEMP TABLE {identifier(temp_tbl_name)}
 (LIKE {table_name}) ON COMMIT DROP;"""

        populate = f"""COPY {identifier(temp_tbl_name)} ({column_names})
 FROM STDIN WITH CSV HEADER;"""

        query = f"""INSERT INTO {identifier(table_name)} ({column_names})
 SELECT * FROM {identifier(temp_tbl_name)}
 ON CONFLICT ({identifier(column_names_array[0])}) DO UPDATE SET"""

        for col in column_names_array:
            logic = f" {identifier(col)} = EXCLUDED.{identifier(col)},"
            if col != column_names_array[0]:
                query += logic

        formatted_query = f"{query[:-1]};"

        conn.run("BEGIN;")
        conn.run(create_temp_tb)
        conn.run(populate, stream=csv_obj)
        conn.run(formatted_query)
        conn.run("COMMIT;")

        return f"File {file_name} loaded."

    except Exception as e:
        raise e

    finally:
        conn.close()
