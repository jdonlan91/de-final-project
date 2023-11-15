resource "aws_sns_topic" "error_alerting" {
  name = "data_pipeline_error_alerting"
}


resource "aws_cloudwatch_log_metric_filter" "ingestor_error" {
    name = "IngestorErrorFilter"
    pattern = "ERROR"
    log_group_name = aws_cloudwatch_log_group.ingestor_log_group.name

    metric_transformation {
      name = "IngestorErrorCount"
      namespace = "Basalt-Ingestor"
      value = "1"
    }
}

resource "aws_cloudwatch_metric_alarm" "alert_ingestor_error" {
    alarm_name = "IngestorErrorAlarm"
    comparison_operator = "GreaterThanOrEqualToThreshold"
    evaluation_periods = 1
    metric_name = "IngestorErrorCount"
    namespace = "Basalt-Ingestor"
    period = 60
    statistic = "Sum"
    threshold = 4
    alarm_description = "Monitors Ingestor Lambda Error occurences"
    alarm_actions = [aws_sns_topic.error_alerting.arn]
    treat_missing_data = "notBreaching"
}



resource "aws_cloudwatch_log_metric_filter" "ingestor_interface_error" {
    name = "IngestorInterfaceErrorFilter"
    pattern = "Error interacting with source database"
    log_group_name = aws_cloudwatch_log_group.ingestor_log_group.name

    metric_transformation {
      name = "IngestorInterfaceErrorCount"
      namespace = "Basalt-Ingestor"
      value = "1"
    }
}

resource "aws_cloudwatch_metric_alarm" "alert_ingestor_interface_error" {
    alarm_name = "IngestorInterfaceErrorAlarm"
    comparison_operator = "GreaterThanOrEqualToThreshold"
    evaluation_periods = 1
    metric_name = "IngestorInterfaceErrorCount"
    namespace = "Basalt-Ingestor"
    period = 60
    statistic = "Sum"
    threshold = 1
    alarm_description = "Monitors Interface Error occurences"
    alarm_actions = [aws_sns_topic.error_alerting.arn]
    treat_missing_data = "notBreaching"
}



resource "aws_cloudwatch_log_metric_filter" "ingestor_resource_not_found_error" {
    name = "IngestorResourceNotFoundError"
    pattern = "Error getting database credentials from Secrets Manager."
    log_group_name = aws_cloudwatch_log_group.ingestor_log_group.name

    metric_transformation {
      name = "IngestorResourceNotFoundErrorCount"
      namespace = "Basalt-Ingestor"
      value = "1"
    }
}

resource "aws_cloudwatch_metric_alarm" "alert_ingestor_resource_not_found_error" {
    alarm_name = "IngestorResourceNotFoundErrorAlarm"
    comparison_operator = "GreaterThanOrEqualToThreshold"
    evaluation_periods = 1
    metric_name = "IngestorResourceNotFoundErrorCount"
    namespace = "Basalt-Ingestor"
    period = 60
    statistic = "Sum"
    threshold = 1
    alarm_description = "Monitors Resource Not Found Error occurences"
    alarm_actions = [aws_sns_topic.error_alerting.arn]
    treat_missing_data = "notBreaching"
}



resource "aws_cloudwatch_log_metric_filter" "ingestor_no_such_bucket_error" {
    name = "IngestorNoSuchBucketError"
    pattern = "Error writing file to ingested bucket."
    log_group_name = aws_cloudwatch_log_group.ingestor_log_group.name

    metric_transformation {
      name = "IngestorNoSuchBucketErrorCount"
      namespace = "Basalt-Ingestor"
      value = "1"
    }
}

resource "aws_cloudwatch_metric_alarm" "alert_ingestor_no_such_bucket_error" {
    alarm_name = "IngestorNoSuchBucketErrorAlarm"
    comparison_operator = "GreaterThanOrEqualToThreshold"
    evaluation_periods = 1
    metric_name = "IngestorNoSuchBucketErrorCount"
    namespace = "Basalt-Ingestor"
    period = 60
    statistic = "Sum"
    threshold = 1
    alarm_description = "Monitors No Such Bucket Error occurences"
    alarm_actions = [aws_sns_topic.error_alerting.arn]
    treat_missing_data = "notBreaching"
}



resource "aws_cloudwatch_log_metric_filter" "ingestor_client_error" {
    name = "IngestorClientError"
    pattern = "AWS client error"
    log_group_name = aws_cloudwatch_log_group.ingestor_log_group.name

    metric_transformation {
      name = "IngestorClientErrorCount"
      namespace = "Basalt-Ingestor"
      value = "1"
    }
}

resource "aws_cloudwatch_metric_alarm" "alert_ingestor_client_error" {
    alarm_name = "IngestorClientErrorAlarm"
    comparison_operator = "GreaterThanOrEqualToThreshold"
    evaluation_periods = 1
    metric_name = "IngestorClientErrorCount"
    namespace = "Basalt-Ingestor"
    period = 60
    statistic = "Sum"
    threshold = 1
    alarm_description = "Monitors Client Error occurences"
    alarm_actions = [aws_sns_topic.error_alerting.arn]
    treat_missing_data = "notBreaching"
}



resource "aws_cloudwatch_log_metric_filter" "ingestor_unexpected_error" {
    name = "IngestorUnexpectedError"
    pattern = "Unexpected error occurred."
    log_group_name = aws_cloudwatch_log_group.ingestor_log_group.name

    metric_transformation {
      name = "IngestorUnexpectedErrorCount"
      namespace = "Basalt-Ingestor"
      value = "1"
    }
}

resource "aws_cloudwatch_metric_alarm" "alert_ingestor_unexpected_error" {
    alarm_name = "IngestorUnexpectedErrorAlarm"
    comparison_operator = "GreaterThanOrEqualToThreshold"
    evaluation_periods = 1
    metric_name = "IngestorUnexpectedErrorCount"
    namespace = "Basalt-Ingestor"
    period = 60
    statistic = "Sum"
    threshold = 1
    alarm_description = "Monitors Unexpected Error occurences"
    alarm_actions = [aws_sns_topic.error_alerting.arn]
    treat_missing_data = "notBreaching"
}


resource "aws_cloudwatch_log_metric_filter" "processor_error" {
    name = "ProcessorErrorFilter"
    pattern = "ERROR"
    log_group_name = aws_cloudwatch_log_group.processor_log_group.name

    metric_transformation {
      name = "ProcessorErrorCount"
      namespace = "Basalt-Processor"
      value = "1"
    }
}

resource "aws_cloudwatch_metric_alarm" "alert_processor_error" {
    alarm_name = "ProcessorErrorAlarm"
    comparison_operator = "GreaterThanOrEqualToThreshold"
    evaluation_periods = 1
    metric_name = "ProcessorErrorCount"
    namespace = "Basalt-Processor"
    period = 60
    statistic = "Sum"
    threshold = 4
    alarm_description = "Monitors processor Lambda Error occurences"
    alarm_actions = [aws_sns_topic.error_alerting.arn]
    treat_missing_data = "notBreaching"
}

resource "aws_cloudwatch_log_metric_filter" "processor_interface_error" {
    name = "ProcessorInterfaceErrorFilter"
    pattern = "Error interacting with database."
    log_group_name = aws_cloudwatch_log_group.processor_log_group.name

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
    metric_name = "ProcessorInterfaceErrorCount"
    namespace = "Basalt-Processor"
    period = 60
    statistic = "Sum"
    threshold = 1
    alarm_description = "Monitors Interface Error occurences"
    alarm_actions = [aws_sns_topic.error_alerting.arn]
    treat_missing_data = "notBreaching"
}



resource "aws_cloudwatch_log_metric_filter" "processor_resource_not_found_error" {
    name = "ProcessorResourceNotFoundError"
    pattern = "Error getting database credentials from Secrets Manager."
    log_group_name = aws_cloudwatch_log_group.processor_log_group.name

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
    metric_name = "ProcessorResourceNotFoundErrorCount"
    namespace = "Basalt-Processor"
    period = 60
    statistic = "Sum"
    threshold = 1
    alarm_description = "Monitors Resource Not Found Error occurences"
    alarm_actions = [aws_sns_topic.error_alerting.arn]
    treat_missing_data = "notBreaching"
}



resource "aws_cloudwatch_log_metric_filter" "processor_no_such_bucket_error" {
    name = "ProcessorNoSuchBucketError"
    pattern = "Error accesing the bucket. NoSuchBucket."
    log_group_name = aws_cloudwatch_log_group.processor_log_group.name

    metric_transformation {
      name = "ProcessorNoSuchBucketErrorCount"
      namespace = "Basalt-Processor"
      value = "1"
    }
}

resource "aws_cloudwatch_metric_alarm" "alert_processor_no_such_bucket_error" {
    alarm_name = "ProcessorNoSuchBucketErrorAlarm"
    comparison_operator = "GreaterThanOrEqualToThreshold"
    evaluation_periods = 1
    metric_name = "ProcessorNoSuchBucketErrorCount"
    namespace = "Basalt-Processor"
    period = 60
    statistic = "Sum"
    threshold = 1
    alarm_description = "Monitors No Such Bucket Error occurences"
    alarm_actions = [aws_sns_topic.error_alerting.arn]
    treat_missing_data = "notBreaching"
}



resource "aws_cloudwatch_log_metric_filter" "processor_client_error" {
    name = "ProcessorClientError"
    pattern = "AWS client error"
    log_group_name = aws_cloudwatch_log_group.processor_log_group.name

    metric_transformation {
      name = "ProcessorClientErrorCount"
      namespace = "Basalt-Processor"
      value = "1"
    }
}

resource "aws_cloudwatch_metric_alarm" "alert_processor_client_error" {
    alarm_name = "ProcessorClientErrorAlarm"
    comparison_operator = "GreaterThanOrEqualToThreshold"
    evaluation_periods = 1
    metric_name = "ProcessorClientErrorCount"
    namespace = "Basalt-Processor"
    period = 60
    statistic = "Sum"
    threshold = 1
    alarm_description = "Monitors Client Error occurences"
    alarm_actions = [aws_sns_topic.error_alerting.arn]
    treat_missing_data = "notBreaching"
}



resource "aws_cloudwatch_log_metric_filter" "processor_unexpected_error" {
    name = "ProcessorUnexpectedError"
    pattern = "Unexpected error occurred."
    log_group_name = aws_cloudwatch_log_group.processor_log_group.name

    metric_transformation {
      name = "ProcessorUnexpectedErrorCount"
      namespace = "Basalt-Processor"
      value = "1"
    }
}

resource "aws_cloudwatch_metric_alarm" "alert_processor_unexpected_error" {
    alarm_name = "ProcessorUnexpectedErrorAlarm"
    comparison_operator = "GreaterThanOrEqualToThreshold"
    evaluation_periods = 1
    metric_name = "ProcessorUnexpectedErrorCount"
    namespace = "Basalt-Processor"
    period = 60
    statistic = "Sum"
    threshold = 1
    alarm_description = "Monitors Unexpected Error occurences"
    alarm_actions = [aws_sns_topic.error_alerting.arn]
    treat_missing_data = "notBreaching"
}


resource "aws_cloudwatch_log_metric_filter" "loader_error" {
    name = "LoaderErrorFilter"
    pattern = "ERROR"
    log_group_name = aws_cloudwatch_log_group.loader_log_group.name

    metric_transformation {
      name = "LoaderErrorCount"
      namespace = "Basalt-Loader"
      value = "1"
    }
}

resource "aws_cloudwatch_metric_alarm" "alert_loader_error" {
    alarm_name = "LoaderErrorAlarm"
    comparison_operator = "GreaterThanOrEqualToThreshold"
    evaluation_periods = 1
    metric_name = "LoaderErrorCount"
    namespace = "Basalt-Loader"
    period = 60
    statistic = "Sum"
    threshold = 4
    alarm_description = "Monitors loader Lambda Error occurences"
    alarm_actions = [aws_sns_topic.error_alerting.arn]
    treat_missing_data = "notBreaching"
}


resource "aws_cloudwatch_log_metric_filter" "loader_interface_error" {
    name = "LoaderInterfaceErrorFilter"
    pattern = "Error interacting with database."
    log_group_name = aws_cloudwatch_log_group.loader_log_group.name

    metric_transformation {
      name = "LoaderInterfaceErrorCount"
      namespace = "Basalt-Loader"
      value = "1"
    }
}

resource "aws_cloudwatch_metric_alarm" "alert_loader_interface_error" {
    alarm_name = "LoaderInterfaceErrorAlarm"
    comparison_operator = "GreaterThanOrEqualToThreshold"
    evaluation_periods = 1
    metric_name = "LoaderInterfaceErrorCount"
    namespace = "Basalt-Loader"
    period = 60
    statistic = "Sum"
    threshold = 1
    alarm_description = "Monitors Interface Error occurences"
    alarm_actions = [aws_sns_topic.error_alerting.arn]
    treat_missing_data = "notBreaching"
}



resource "aws_cloudwatch_log_metric_filter" "loader_resource_not_found_error" {
    name = "LoaderResourceNotFoundError"
    pattern = "Error getting database credentials from Secrets Manager."
    log_group_name = aws_cloudwatch_log_group.loader_log_group.name

    metric_transformation {
      name = "loaderResourceNotFoundErrorCount"
      namespace = "Basalt-Loader"
      value = "1"
    }
}

resource "aws_cloudwatch_metric_alarm" "alert_loader_resource_not_found_error" {
    alarm_name = "LoaderResourceNotFoundErrorAlarm"
    comparison_operator = "GreaterThanOrEqualToThreshold"
    evaluation_periods = 1
    metric_name = "loaderResourceNotFoundErrorCount"
    namespace = "Basalt-Loader"
    period = 60
    statistic = "Sum"
    threshold = 1
    alarm_description = "Monitors Resource Not Found Error occurences"
    alarm_actions = [aws_sns_topic.error_alerting.arn]
    treat_missing_data = "notBreaching"
}



resource "aws_cloudwatch_log_metric_filter" "loader_no_such_bucket_error" {
    name = "LoaderNoSuchBucketError"
    pattern = "Error accesing the bucket. NoSuchBucket."
    log_group_name = aws_cloudwatch_log_group.loader_log_group.name

    metric_transformation {
      name = "loaderNoSuchBucketErrorCount"
      namespace = "Basalt-Loader"
      value = "1"
    }
}

resource "aws_cloudwatch_metric_alarm" "alert_loader_no_such_bucket_error" {
    alarm_name = "loaderNoSuchBucketErrorAlarm"
    comparison_operator = "GreaterThanOrEqualToThreshold"
    evaluation_periods = 1
    metric_name = "loaderNoSuchBucketErrorCount"
    namespace = "Basalt-Loader"
    period = 60
    statistic = "Sum"
    threshold = 1
    alarm_description = "Monitors No Such Bucket Error occurences"
    alarm_actions = [aws_sns_topic.error_alerting.arn]
    treat_missing_data = "notBreaching"
}



resource "aws_cloudwatch_log_metric_filter" "loader_client_error" {
    name = "LoaderClientError"
    pattern = "AWS client error"
    log_group_name = aws_cloudwatch_log_group.loader_log_group.name

    metric_transformation {
      name = "loaderClientErrorCount"
      namespace = "Basalt-Loader"
      value = "1"
    }
}

resource "aws_cloudwatch_metric_alarm" "alert_loader_client_error" {
    alarm_name = "LoaderClientErrorAlarm"
    comparison_operator = "GreaterThanOrEqualToThreshold"
    evaluation_periods = 1
    metric_name = "loaderClientErrorCount"
    namespace = "Basalt-Loader"
    period = 60
    statistic = "Sum"
    threshold = 1
    alarm_description = "Monitors Client Error occurences"
    alarm_actions = [aws_sns_topic.error_alerting.arn]
    treat_missing_data = "notBreaching"
}



resource "aws_cloudwatch_log_metric_filter" "loader_unexpected_error" {
    name = "LoaderUnexpectedError"
    pattern = "Unexpected error occurred."
    log_group_name = aws_cloudwatch_log_group.loader_log_group.name

    metric_transformation {
      name = "loaderUnexpectedErrorCount"
      namespace = "Basalt-Loader"
      value = "1"
    }
}

resource "aws_cloudwatch_metric_alarm" "alert_loader_unexpected_error" {
    alarm_name = "LoaderUnexpectedErrorAlarm"
    comparison_operator = "GreaterThanOrEqualToThreshold"
    evaluation_periods = 1
    metric_name = "loaderUnexpectedErrorCount"
    namespace = "Basalt-Loader"
    period = 60
    statistic = "Sum"
    threshold = 1
    alarm_description = "Monitors Unexpected Error occurences"
    alarm_actions = [aws_sns_topic.error_alerting.arn]
    treat_missing_data = "notBreaching"
}
