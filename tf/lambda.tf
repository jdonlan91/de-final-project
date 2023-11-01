resource "aws_lambda_function" "ingester" {
    function_name = "ingester"
    filename = "${path.module}/../src/ingester/ingester_payload.zip"
    #layers = []
    role = aws_iam_role.ingestor_lambda_role.arn
    handler = "ingester.lambda_handler"
    runtime = "python3.11"
}