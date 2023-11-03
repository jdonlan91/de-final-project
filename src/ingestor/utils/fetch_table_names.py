from pg8000.native import Connection, identifier, literal


def create_connection(db_credentials):
    return Connection(
        user=db_credentials["DB_USERNAME"],
        password=db_credentials["DB_PASSWORD"],
        host=db_credentials["DB_HOST"],
        database=db_credentials["DB_NAME"],
    )
    

def fetch_table_names(db_name, db_credentials):
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
    conn = create_connection(db_credentials)
    