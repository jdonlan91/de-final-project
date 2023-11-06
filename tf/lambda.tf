resource "aws_lambda_function" "ingestor" {
    function_name = "ingestor"
    filename = data.archive_file.ingestor_lambda.output_path
    layers = [aws_lambda_layer_version.ingestor_utils_layer.arn, "arn:aws:lambda:eu-west-2:336392948345:layer:AWSSDKPandas-Python311:2"]
    role = aws_iam_role.ingestor_lambda_role.arn
    handler = "ingestor.lambda_handler"
    source_code_hash = data.archive_file.ingestor_lambda.output_base64sha256
    runtime = "python3.11"
}


resource "aws_lambda_layer_version" "ingestor_utils_layer" {
    filename = data.archive_file.ingestor_utils.output_path
    layer_name = "ingestor_utils_layer"
    source_code_hash = data.archive_file.ingestor_utils.output_base64sha256
}