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

resource "aws_cloudwatch_metric_alarm" "alert_resource_not_found_error" {
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



resource "aws_cloudwatch_log_metric_filter" "client_error" {
    name = "ClientError"
    pattern = "AWS client error"
    log_group_name = "/aws/lambda/ingestor"

    metric_transformation {
      name = "ClientErrorCount"
      namespace = "Basalt-Ingestor"
      value = "1"
    }
}

resource "aws_cloudwatch_metric_alarm" "alert_client_error" {
    alarm_name = "ClientErrorAlarm"
    comparison_operator = "GreaterThanOrEqualToThreshold"
    evaluation_periods = 1
    metric_name = aws_cloudwatch_log_metric_filter.client_error.id
    namespace = "Basalt-Ingestor"
    period = 60
    statistic = "Sum"
    threshold = 1
    alarm_description = "Monitors Client Error occurences"
    insufficient_data_actions = []
}



resource "aws_cloudwatch_log_metric_filter" "unexpected_error" {
    name = "UnexpectedError"
    pattern = "Unexpected error occurred."
    log_group_name = "/aws/lambda/ingestor"

    metric_transformation {
      name = "UnexpectedErrorCount"
      namespace = "Basalt-Ingestor"
      value = "1"
    }
}

resource "aws_cloudwatch_metric_alarm" "alert_unexpected_error" {
    alarm_name = "UnexpectedErrorAlarm"
    comparison_operator = "GreaterThanOrEqualToThreshold"
    evaluation_periods = 1
    metric_name = aws_cloudwatch_log_metric_filter.unexpected_error.id
    namespace = "Basalt-Ingestor"
    period = 60
    statistic = "Sum"
    threshold = 1
    alarm_description = "Monitors Unexpected Error occurences"
    insufficient_data_actions = []
}

resource "aws_cloudwatch_log_metric_filter" "processor_interface_error" {
    name = "ProcessorInterfaceErrorFilter"
    pattern = "Error interacting with database."
    log_group_name = "/aws/lambda/processor"

    metric_transformation {
      name = "ProcessorInterfaceErrorCount"
      namespace = "Basalt-Processor"
      value = "1"
    }
}

resource "aws_cloudwatch_metric_alarm" "alert_processor_interface_error" {
    alarm_name = "ProcessorInterfaceErrorAlarm"
    comparison_operator = "GreaterThanOrEqualToThreshold"
    evaluation_periods = 1
    metric_name = aws_cloudwatch_log_metric_filter.processor_interface_error.id
    namespace = "Basalt-Processor"
    period = 60
    statistic = "Sum"
    threshold = 1
    alarm_description = "Monitors Interface Error occurences"
    insufficient_data_actions = []
}



resource "aws_cloudwatch_log_metric_filter" "processor_resource_not_found_error" {
    name = "ProcessorResourceNotFoundError"
    pattern = "Error getting database credentials from Secrets Manager."
    log_group_name = "/aws/lambda/processor"

    metric_transformation {
      name = "ProcessorResourceNotFoundErrorCount"
      namespace = "Basalt-Processor"
      value = "1"
    }
}

resource "aws_cloudwatch_metric_alarm" "alert_processor_resource_not_found_error" {
    alarm_name = "ProcessorResourceNotFoundErrorAlarm"
    comparison_operator = "GreaterThanOrEqualToThreshold"
    evaluation_periods = 1
    metric_name = aws_cloudwatch_log_metric_filter.processor_resource_not_found_error.id
    namespace = "Basalt-Processor"
    period = 60
    statistic = "Sum"
    threshold = 1
    alarm_description = "Monitors Resource Not Found Error occurences"
    insufficient_data_actions = []
}



resource "aws_cloudwatch_log_metric_filter" "processor_no_such_bucket_error" {
    name = "ProcessorNoSuchBucketError"
    pattern = "Error accesing the bucket. NoSuchBucket."
    log_group_name = "/aws/lambda/processor"

    metric_transformation {
      name = "ProcessorNoSuchBucketErrorCount"
      namespace = "Basalt-Processor"
      value = "1"
    }
}

resource "aws_cloudwatch_metric_alarm" "processor_alert_no_such_bucket_error" {
    alarm_name = "ProcessorNoSuchBucketErrorAlarm"
    comparison_operator = "GreaterThanOrEqualToThreshold"
    evaluation_periods = 1
    metric_name = aws_cloudwatch_log_metric_filter.processor_no_such_bucket_error.id
    namespace = "Basalt-Processor"
    period = 60
    statistic = "Sum"
    threshold = 1
    alarm_description = "Monitors No Such Bucket Error occurences"
    insufficient_data_actions = []
}



resource "aws_cloudwatch_log_metric_filter" "processor_client_error" {
    name = "ProcessorClientError"
    pattern = "AWS client error"
    log_group_name = "/aws/lambda/processor"

    metric_transformation {
      name = "ProcessorClientErrorCount"
      namespace = "Basalt-Processor"
      value = "1"
    }
}

resource "aws_cloudwatch_metric_alarm" "processor_alert_client_error" {
    alarm_name = "ProcessorClientErrorAlarm"
    comparison_operator = "GreaterThanOrEqualToThreshold"
    evaluation_periods = 1
    metric_name = aws_cloudwatch_log_metric_filter.processor_client_error.id
    namespace = "Basalt-Processor"
    period = 60
    statistic = "Sum"
    threshold = 1
    alarm_description = "Monitors Client Error occurences"
    insufficient_data_actions = []
}



resource "aws_cloudwatch_log_metric_filter" "processor_unexpected_error" {
    name = "ProcessorUnexpectedError"
    pattern = "Unexpected error occurred."
    log_group_name = "/aws/lambda/processor"

    metric_transformation {
      name = "ProcessorUnexpectedErrorCount"
      namespace = "Basalt-Processor"
      value = "1"
    }
}

resource "aws_cloudwatch_metric_alarm" "processor_alert_unexpected_error" {
    alarm_name = "ProcessorUnexpectedErrorAlarm"
    comparison_operator = "GreaterThanOrEqualToThreshold"
    evaluation_periods = 1
    metric_name = aws_cloudwatch_log_metric_filter.processor_unexpected_error.id
    namespace = "Basalt-Processor"
    period = 60
    statistic = "Sum"
    threshold = 1
    alarm_description = "Monitors Unexpected Error occurences"
    insufficient_data_actions = []
}
