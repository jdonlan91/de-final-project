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
    threshold = 1
    alarm_description = "Monitors Interface Error occurences"
    insufficient_data_actions = []
}



resource "aws_cloudwatch_log_metric_filter" "resource_not_found_error" {
    name = "ResourceNotFoundError"
    pattern = "Error getting database credentials from Secrets Manager."
    log_group_name = "/aws/lambda/ingestor"

    metric_transformation {
      name = "ResourceNotFoundErrorCount"
      namespace = "Basalt-Ingestor"
      value = "1"
    }
}

resource "aws_cloudwatch_metric_alarm" "alert_interface_error" {
    alarm_name = "ResourceNotFoundErrorAlarm"
    comparison_operator = "GreaterThanOrEqualToThreshold"
    evaluation_periods = 1
    metric_name = aws_cloudwatch_log_metric_filter.resource_not_found_error.id
    namespace = "Basalt-Ingestor"
    period = 60
    statistic = "Sum"
    threshold = 1
    alarm_description = "Monitors Resource Not Found Error occurences"
    insufficient_data_actions = []
}



resource "aws_cloudwatch_log_metric_filter" "no_such_bucket_error" {
    name = "NoSuchBucketError"
    pattern = "Error writing file to ingested bucket."
    log_group_name = "/aws/lambda/ingestor"

    metric_transformation {
      name = "NoSuchBucketErrorCount"
      namespace = "Basalt-Ingestor"
      value = "1"
    }
}

resource "aws_cloudwatch_metric_alarm" "alert_no_such_bucket_error" {
    alarm_name = "NoSuchBucketErrorAlarm"
    comparison_operator = "GreaterThanOrEqualToThreshold"
    evaluation_periods = 1
    metric_name = aws_cloudwatch_log_metric_filter.no_such_bucket_error.id
    namespace = "Basalt-Ingestor"
    period = 60
    statistic = "Sum"
    threshold = 1
    alarm_description = "Monitors No Such Bucket Error occurences"
    insufficient_data_actions = []
}
