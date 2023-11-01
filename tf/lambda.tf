resource "aws_lambda_function" "ingester" {
    function_name = "ingester"
    filename = "${path.module}/../src/ingester/ingester_payload.zip"
    layers = [aws_lambda_layer_version.ingester_utils_layer.arn]
    role = aws_iam_role.ingestor_lambda_role.arn
    handler = "ingester.lambda_handler"
    runtime = "python3.11"
}


resource "aws_lambda_layer_version" "ingester_utils_layer" {
    filename = "${path.module}/../src/ingester/utils_payload.zip"
    layer_name = "ingester_utils_layer"
}