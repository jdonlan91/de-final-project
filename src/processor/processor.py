def lambda_handler(event, context):
    """
    Takes data from ingested bucket, transforms and converts the data
    into parquet and dumps the data into processed bucket.
    
    Triggered by s3:CreateObject when a new file is dumped into 
    the ingested bucket.

    Calls read_csv util function to read ingested data.
    Calls transform_data util function to transform data into relevant schema.
    Calls convert_and_dump_parquet util function to dump parquet files
    into processed bucket.
    Logs metadata about files added to the processed bucket.
    Logs any errors that occur.
        
        
        
    """
    pass
