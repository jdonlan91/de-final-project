from pg8000.native import Connection, literal
from datetime import date, timedelta


def create_connection(db_credentials):
    return Connection(
        user=db_credentials["DB_USERNAME"],
        password=db_credentials["DB_PASSWORD"],
        host=db_credentials["DB_HOST"],
        database=db_credentials["DB_NAME"],
    )


def seed_dim_date(db_credentials):
    conn = create_connection(db_credentials)
    starting_date = date(2022, 1, 1)
    current_date = starting_date

    while current_date <= date(2024, 12, 31):
        example_date = current_date
        date_id = example_date
        year = example_date.year
        month = example_date.month
        day = example_date.day
        day_of_week = example_date.isoweekday()
        day_name = example_date.strftime('%A')
        month_name = example_date.strftime('%B')
        quarter = ((example_date.month - 1)//3) + 1

        query = f"""INSERT INTO dim_date
(date_id, year, month, day, day_of_week, day_name, month_name, quarter)
VALUES ({literal(date_id)}, {literal(year)}, {literal(month)},
{literal(day)}, {literal(day_of_week)}, {literal(day_name)},
{literal(month_name)}, {literal(quarter)});"""

        conn.run(query)
        current_date += timedelta(1)
