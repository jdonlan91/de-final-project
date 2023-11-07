resource "aws_cloudwatch_log_metric_filter" "interface_error" {
    name = "InterfaceErrorFilter"
    pattern = "Error interacting with source database"
    log_group_name = "/aws/lambda/ingestor"

    metric_transformation {
      name = "InterfaceErrorCount"
      namespace = "Basalt-Ingestor"
      value = "1"
    }
}

resource "aws_cloudwatch_metric_alarm" "alert_interface_error" {
    alarm_name = "InterfaceErrorAlarm"
    comparison_operator = "GreaterThanOrEqualToThreshold"
    evaluation_periods = 1
    metric_name = aws_cloudwatch_log_metric_filter.interface_error.id
    namespace = "Basalt-Ingestor"
    period = 60
    statistic = "Sum"
    threshold = 4
    alarm_description = "Monitors Interface Error occurences"
    insufficient_data_actions = []
}