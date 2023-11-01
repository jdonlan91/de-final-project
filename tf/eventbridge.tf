resource "aws_cloudwatch_event_rule" "ingestor_schedule" {
    schedule_expression = "rate(5 minutes)"
}

resource "aws_cloudwatch_event_target" "ingestor_target" {
    arn = aws_lambda_function.ingestor.arn
    rule = aws_cloudwatch_event_rule.ingestor_schedule.name
}

resource "aws_lambda_permission" "ingestor_eventbridge_permission" {
    action = "lambda:InvokeFunction"
    function_name = aws_lambda_function.ingestor.function_name
    principal = "events.amazonaws.com"
    source_arn = aws_cloudwatch_event_rule.ingestor_schedule.arn
}