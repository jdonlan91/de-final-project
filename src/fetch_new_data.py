# To allow us to identify new data that has appeared
# since the last invocation of this function on a particular table,
# we can use use a WHERE clause for the last_updated column (if it exists)

# Depending on the how often this function is called (e.g. every 1 min)
# we can use the current timestamp, subtracting that interval in the clause.
# ! If we do this, we'd probably need a second parameter for the interval !

# The ERD shows that all the production tables have a last_updated column
def fetch_new_data(table_name: str) -> list[dict]:
    """Selects data with SQL from a specified table
    and returns the rows as a list of dictionaries

        Parameters:
                table_name <string>: The table name

        Returns:
                <list[dict]>
    """
    pass
