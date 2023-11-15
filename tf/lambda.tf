resource "aws_lambda_function" "ingestor" {
    function_name = "ingestor"
    filename = data.archive_file.ingestor_lambda.output_path
    layers = [aws_lambda_layer_version.ingestor_utils_layer.arn,
    "arn:aws:lambda:eu-west-2:336392948345:layer:AWSSDKPandas-Python311:2",
    aws_lambda_layer_version.pg8000_layer.arn]
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

resource "aws_cloudwatch_log_group" "ingestor_log_group" {
  name = "/aws/lambda/ingestor"
  }

resource "aws_cloudwatch_log_stream" "ingestor_history" {
  name           = "ingestor_history"
  log_group_name = aws_cloudwatch_log_group.ingestor_log_group.name
}

resource "aws_lambda_layer_version" "pg8000_layer" {
    filename = "${path.module}/../src/pg8000.zip"
    layer_name = "pg8000_layer"
}

resource "aws_lambda_function" "processor" {
    function_name = "processor"
    filename = data.archive_file.processor_lambda.output_path
    layers = [aws_lambda_layer_version.processor_utils_layer.arn,
    aws_lambda_layer_version.processor_ccy_layer.arn,
    "arn:aws:lambda:eu-west-2:336392948345:layer:AWSSDKPandas-Python311:2",
    aws_lambda_layer_version.pg8000_layer.arn]
    role = aws_iam_role.processor_lambda_role.arn
    handler = "processor.lambda_handler"
    source_code_hash = data.archive_file.processor_lambda.output_base64sha256
    runtime = "python3.11"
    timeout = 300

    environment {
      variables = {
        PROCESSED_BUCKET_NAME = aws_s3_bucket.processed_bucket.id
      }
    }
}

resource "aws_cloudwatch_log_group" "processor_log_group" {
  name = "/aws/lambda/processor"
  }


resource "aws_lambda_layer_version" "processor_utils_layer" {
    filename = data.archive_file.processor_utils.output_path
    layer_name = "processor_utils_layer"
    source_code_hash = data.archive_file.processor_utils.output_base64sha256
}

resource "aws_lambda_layer_version" "processor_ccy_layer" {
    filename = "${path.module}/../src/processor/ccy.zip"
    layer_name = "processor_ccy_layer"
}

resource "aws_lambda_permission" "allow_s3_ingested_to_invoke_processor" {
  action = "lambda:InvokeFunction"
  function_name = aws_lambda_function.processor.function_name
  principal = "s3.amazonaws.com"
  source_arn = aws_s3_bucket.ingested_bucket.arn
}


resource "aws_lambda_function" "loader" {
    function_name = "loader"
    filename = data.archive_file.loader_lambda.output_path
    layers = [aws_lambda_layer_version.loader_utils_layer.arn,
    aws_lambda_layer_version.pg8000_layer.arn,
    "arn:aws:lambda:eu-west-2:336392948345:layer:AWSSDKPandas-Python311:2"]
    role = aws_iam_role.loader_lambda_role.arn
    handler = "loader.lambda_handler"
    source_code_hash = data.archive_file.loader_lambda.output_base64sha256
    runtime = "python3.11"
    timeout = 300
}

resource "aws_cloudwatch_log_group" "loader_log_group" {
  name = "/aws/lambda/loader"
  }


resource "aws_lambda_layer_version" "loader_utils_layer" {
    filename = data.archive_file.loader_utils.output_path
    layer_name = "loader_utils_layer"
    source_code_hash = data.archive_file.loader_utils.output_base64sha256
}


resource "aws_cloudwatch_log_stream" "loader_history" {
  name           = "loader_history"
  log_group_name = aws_cloudwatch_log_group.loader_log_group.name
}
