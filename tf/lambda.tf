resource "aws_lambda_function" "ingestor" {
    function_name = "ingestor"
    filename = "${path.module}/../src/ingestor/ingestor_payload.zip"
    layers = [aws_lambda_layer_version.ingestor_utils_layer.arn]
    role = aws_iam_role.ingestor_lambda_role.arn
    handler = "ingestor.lambda_handler"
    source_code_hash = data.archive_file.ingestor_lambda.output_base64sha256
    runtime = "python3.11"
}


resource "aws_lambda_layer_version" "ingestor_utils_layer" {
    filename = "${path.module}/../src/ingestor/utils_payload.zip"
    layer_name = "ingestor_utils_layer"
    source_code_hash = data.archive_file.ingestor_utils.output_base64sha256
}


resource "aws_cloudwatch_log_stream" "ingestor_history" {
  name           = "ingestor_history"
  log_group_name = "/aws/lambda/${aws_lambda_function.ingestor.function_name}"
}