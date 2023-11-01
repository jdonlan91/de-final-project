import pandas as pd


def convert_to_csv(list_of_dictionaries):
    """Converts list of dictionaries to csv.

    Takes a list of dictionaries from fetch_new_data with the data from
    one of the database tables and converts it to a csv format string with
    the keys as table columns.

    Args:
        list_of_dictionaries

    Returns:
        csv string. For example:
        "staff_id,first_name\n1,Jeremie\n2,Peter\n3,Steve\n4,Mary\n"

    Raises:
        Exception.
    """

    if len(list_of_dictionaries) == 0:
        return ""

    try:
        df = pd.DataFrame(list_of_dictionaries)
        csv_string = df.to_csv(index=False)
        return csv_string

    except Exception as e:
        raise e
