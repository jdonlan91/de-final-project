from pg8000.native import Connection, identifier, literal


def create_connection(db_credentials):
    return Connection(
        user=db_credentials["DB_USERNAME"],
        password=db_credentials["DB_PASSWORD"],
        host=db_credentials["DB_HOST"],
        database=db_credentials["DB_NAME"],
    )
    

def fetch_table_names(db_name, db_credentials):
    """Fetches table names from database for lambda_handler function
    
    Args:
        database_name <string> the name of the database to fetch the table names
    
    Returns:
        <list> a list of table names in the database
    
    Reads and fetches all the table names from a given database, 
    returning them in a list.
    """
    conn = create_connection(db_credentials)
    