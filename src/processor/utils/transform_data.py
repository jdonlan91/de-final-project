import json
import ccy
import boto3
from pg8000.native import Connection, identifier, literal


def get_db_credentials():
    secret_name = "totesys_db_credentials"
    region_name = "eu-west-2"

    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager",
                            region_name=region_name)

    get_secret_value_response = client.get_secret_value(SecretId=secret_name)

    secret = json.loads(get_secret_value_response["SecretString"])
    db_credentials = {}
    db_credentials["DB_HOST"] = secret["host"]
    db_credentials["DB_USERNAME"] = secret["username"]
    db_credentials["DB_PASSWORD"] = secret["password"]
    db_credentials["DB_NAME"] = secret["dbname"]

    return db_credentials


def create_connection(db_credentials):
    return Connection(
        user=db_credentials["DB_USERNAME"],
        password=db_credentials["DB_PASSWORD"],
        host=db_credentials["DB_HOST"],
        database=db_credentials["DB_NAME"],
    )


def query_database(table_name, column_name, foreign_key, foreign_key_value):
    db_credentials = get_db_credentials()
    conn = create_connection(db_credentials)

    query = f"""
        SELECT {identifier(column_name)}
        FROM {identifier(table_name)}
        WHERE {identifier(foreign_key)} = {literal(foreign_key_value)}
    """

    query_result = conn.run(query)

    return query_result[0][0]


def transform_counterparty(data):
    transformed_data = [
        {
            "counterparty_id": row["counterparty_id"],
            "counterparty_legal_name": row["counterparty_legal_name"],
            "counterparty_legal_address_line_1": query_database(
                table_name="address",
                column_name="address_line_1",
                foreign_key="address_id",
                foreign_key_value=row["legal_address_id"]
            ),
            "counterparty_legal_address_line_2": query_database(
                table_name="address",
                column_name="address_line_2",
                foreign_key="address_id",
                foreign_key_value=row["legal_address_id"]
            ),
            "counterparty_legal_district": query_database(
                table_name="address",
                column_name="district",
                foreign_key="address_id",
                foreign_key_value=row["legal_address_id"]
            ),
            "counterparty_legal_city": query_database(
                table_name="address",
                column_name="city",
                foreign_key="address_id",
                foreign_key_value=row["legal_address_id"]
            ),
            "counterparty_legal_postal_code": query_database(
                table_name="address",
                column_name="district",
                foreign_key="postal_code",
                foreign_key_value=row["legal_address_id"]
            ),
            "counterparty_legal_country": query_database(
                table_name="address",
                column_name="country",
                foreign_key="address_id",
                foreign_key_value=row["legal_address_id"]
            ),
            "counterparty_legal_phone_number": query_database(
                table_name="address",
                column_name="phone",
                foreign_key="address_id",
                foreign_key_value=row["legal_address_id"]
            )
        }
        for row in data
    ]

    return transformed_data


def transform_currency(data):

    transformed_data = [
        {
            "currency_id": row["currency_id"],
            "currency_code": row["currency_code"],
            "currency_name": ccy.currency(row["currency_code"]).name
        }
        for row in data
    ]

    return transformed_data


def transform_department():
    pass


def transform_design(data):
    transformed_data = [
        {
            "design_id": row["design_id"],
            "design_name": row["design_name"],
            "file_location": row["file_location"],
            "file_name": row["file_name"]
        }
        for row in data
    ]

    return transformed_data


def transform_staff(data):
    transformed_data = [
        {
            "staff_id": row["staff_id"],
            "first_name": row["first_name"],
            "last_name": row["last_name"],
            "department_name": query_database(
                table_name="department",
                column_name="department_name",
                foreign_key="department_id",
                foreign_key_value=row["department_id"]
            ),
            "location": query_database(
                table_name="department",
                column_name="location",
                foreign_key="department_id",
                foreign_key_value=row["department_id"]
            ),
            "email_address": row["email_address"]
        }
        for row in data
    ]

    return transformed_data


def transform_sales_order(data):
    transformed_data = [
        {
            "sales_order_id": row["sales_order_id"],
            "created_date": row["created_at"][:10],
            "created_time": row["created_at"][11:],
            "last_updated_date": row["last_updated"][:10],
            "last_updated_time": row["last_updated"][11:],
            "sales_staff_id": row["staff_id"],
            "counterparty_id": row["counterparty_id"],
            "units_sold": row["units_sold"],
            "unit_price": row["unit_price"],
            "currency_id": row["currency_id"],
            "design_id": row["design_id"],
            "agreed_payment_date": row["agreed_payment_date"],
            "agreed_delivery_date": row["agreed_delivery_date"],
            "agreed_delivery_location_id": row["agreed_delivery_location_id"]
        }
        for row in data
    ]

    return transformed_data


def transform_address(data):
    transformed_data = [
        {
            "location_id": row["address_id"],
            "address_line_1": row["address_line_1"],
            "address_line_2": row["address_line_2"],
            "district": row["district"],
            "city": row["city"],
            "postal_code": row["postal_code"],
            "country": row["country"],
            "phone": row["phone"],
        }
        for row in data
    ]

    return transformed_data


# def transform_payment():
#     pass


# def transform_purchase_order():
#     pass


# def transform_payment_type():
#     pass


# def transform_transaction():
#     pass


def transform_data(file_name, data):
    pass


transform_currency()
