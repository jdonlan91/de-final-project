from pg8000.native import Connection


def create_connection(db_credentials):
    return Connection(
        user=db_credentials["DB_USERNAME"],
        password=db_credentials["DB_PASSWORD"],
        host=db_credentials["DB_HOST"],
        database=db_credentials["DB_NAME"],
    )


def flatten_single_subitem_list(list_of_lists):
    return [item[0] for item in list_of_lists]


def fetch_table_names(db_credentials):
    """Reads and fetches all the table names from a given database,
    returning them in a list.

    Args:
        db_name <string> the name of the database to fetch the table names
        db_credentials <dictionary>: credentials for accessing the database.
        Credentials needs to be in the following format:
            {
                "DB_USERNAME": ...
                "DB_NAME": ...
                "DB_HOST": ...
                "DB_PASSWORD": ...
            }

    Returns:
        <list> a list of table names in the database
    """
    try:
        conn = create_connection(db_credentials)

        query = """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name NOT LIKE '_prisma_migrations'
        """
        query_result = conn.run(query)

        return flatten_single_subitem_list(query_result)

    finally:
        if conn:
            close.conn()
