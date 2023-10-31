import pandas as pd


def convert_to_csv(list_of_dictionaries):
    """Takes a list of dictionaries from fetch_new_data with the data from
    one of the database tables and converts it to a csv format string with
    keys as table columns

    Parameters:
        list_of_dictionaries

    Returns:
        csv string
    """
    if len(list_of_dictionaries) == 0:
        return ""
    try:
        df = pd.DataFrame(list_of_dictionaries)
        csv_string = df.to_csv(index=False)
        return csv_string
    except Exception as e:
        raise e
