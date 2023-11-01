from os import environ
from pg8000.native import Connection, identifier, literal
from dotenv import load_dotenv

# To allow us to identify new data that has appeared
# since the last invocation of this function on a particular table,
# we can use use a WHERE clause for the last_updated column (if it exists)

# Depending on the how often this function is called (e.g. every 1 min)
# we can use the current timestamp, subtracting that interval in the clause.
# ! If we do this, we'd probably need a second parameter for the interval !

# The ERD shows that all the production tables have a last_updated column


def fetch_new_data(table_name: str, timestamp, db_credentials) -> list[dict]:
    """Selects data with SQL from a specified table
    and returns the rows as a list of dictionaries

        Parameters:
                table_name <string>: The table name

        Returns:
                <list[dict]>
    """
    conn = Connection(
        user=db_credentials["DB_USERNAME"], password=db_credentials[
            "DB_PASSWORD"], host=db_credentials["DB_HOST"], database=db_credentials["DB_NAME"]
    )

#     print(conn.columns)
    query = f'''SELECT * FROM {identifier(table_name)}
                       WHERE last_updated > {literal(timestamp)}'''
    results_list_of_lists = conn.run(query)
    column_names = [column['name'] for column in conn.columns]
    results_list_of_dicts = []
    for row in results_list_of_lists:
        row_dictionary = {}
        for i in range(len(column_names)):
            row_dictionary[column_names[i]] = row[i]
        results_list_of_dicts.append(row_dictionary)
    return results_list_of_dicts
