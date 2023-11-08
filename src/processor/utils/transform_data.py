# This module has a set of functions that transform from a normalised format
# to a denormalised format.
# Takes data from ingested bucket (corresponds to one source table)
# (sometimes) queries source database to get additional data
# transforms data into star schema
# returns transformed data as list-of-dictionaries


# def transform_counterparty():
#     pass


# def transform_currency():
#     pass


# def transform_department():
#     pass


# def transform_design():
#     pass


# def transform_staff():
#     pass


def transform_sales_order(data):
    transformed_data = []

    for row in data:
        transformed_row = {
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
            "agreed_delivery_location_id": row["agreed_delivery_location_id"],
        }

        transformed_data.append(transformed_row)

    return transformed_data


# def transform_address():
#     pass


# def transform_payment():
#     pass


# def transform_purchase_order():
#     pass


# def transform_payment_type():
#     pass


# def transform_transaction():
#     pass
