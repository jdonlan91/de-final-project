resource "aws_lambda_function" "ingestor" {
    function_name = "ingestor"
    filename = data.archive_file.ingestor_lambda.output_path
    layers = [aws_lambda_layer_version.ingestor_utils_layer.arn,
    "arn:aws:lambda:eu-west-2:336392948345:layer:AWSSDKPandas-Python311:2",
    aws_lambda_layer_version.ingestor_pg8000_layer.arn]
    role = aws_iam_role.ingestor_lambda_role.arn
    handler = "ingestor.lambda_handler"
    source_code_hash = data.archive_file.ingestor_lambda.output_base64sha256
    runtime = "python3.11"
    timeout = 300
}


resource "aws_lambda_layer_version" "ingestor_utils_layer" {
    filename = data.archive_file.ingestor_utils.output_path
    layer_name = "ingestor_utils_layer"
    source_code_hash = data.archive_file.ingestor_utils.output_base64sha256
}

resource "aws_cloudwatch_log_stream" "ingestor_history" {
  name           = "ingestor_history"
  log_group_name = "/aws/lambda/${aws_lambda_function.ingestor.function_name}"
}

resource "aws_lambda_layer_version" "ingestor_pg8000_layer" {
    filename = "${path.module}/../src/ingestor/pg8000.zip"
    layer_name = "ingestor_pg8000_layer"
}


resource "aws_lambda_function" "processor" {
    function_name = "processor"
    filename = data.archive_file.processor_lambda.output_path
    layers = []
    role = aws_iam_role.processor_lambda_role.arn
    handler = "processor.lambda_handler"
    source_code_hash = data.archive_file.processor_lambda.output_base64sha256
    runtime = "python3.11"
    timeout = 300
}


resource "aws_lambda_permission" "allow_s3_ingested_to_invoke_processor" {
  action = "lambda:InvokeFunction"
  function_name = aws_lambda_function.processor.function_name
  principal = "s3.amazonaws.com"
  source_arn = aws_s3_bucket.ingested_bucket.arn
}