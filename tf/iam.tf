resource "aws_iam_policy" "s3_ingested_write_policy" {
  name        = "S3WritePolicyForIngested"
  description = "Policy for writing to Ingested Bucket"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "s3:PutObject"
        ],
        Resource = "${aws_s3_bucket.ingested_bucket.arn}/*"
      }
    ]
  })
}

resource "aws_iam_policy" "ingestor_history_logging_policy" {
  name        = "HistoryLoggingPolicyForIngestor"
  description = "Policy for logging and reading invocation history of Ingestor"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "logs:PutLogEvents",
          "logs:GetLogEvents",
        ],
        Resource = "${aws_cloudwatch_log_stream.ingestor_history.arn}"
      }
    ]
  })
}

resource "aws_iam_policy" "ingestor_logging_policy" {
  name        = "LoggingPolicyForIngestor"
  description = "Policy for logging behaviour of Ingestor"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "logs:PutLogEvents",
          "logs:CreateLogStream",
          "logs:CreateLogGroup",
        ],
        Resource = "arn:aws:logs:eu-west-2:144630460963:log-group:/aws/lambda/ingestor:*"
      }
    ]
  })
}


resource "aws_iam_policy" "s3_ingested_read_policy" {
  name        = "S3ReadPolicyForIngested"
  description = "Policy for reading from Ingested Bucket"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "s3:GetObject"
        ],
        Resource = "${aws_s3_bucket.ingested_bucket.arn}/*"
      }
    ]
  })
}


resource "aws_iam_policy" "s3_processed_write_policy" {
  name        = "S3WritePolicyForProcessed"
  description = "Policy for writing to Processed Bucket"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "s3:PutObject"
        ],
        Resource = "${aws_s3_bucket.processed_bucket.arn}/*"
      }
    ]
  })
}


resource "aws_iam_policy" "processor_logging_policy" {
  name        = "LoggingPolicyForProcessor"
  description = "Policy for logging behaviour of Processor"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "logs:PutLogEvents",
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
        ],
        Resource = "arn:aws:logs:eu-west-2:144630460963:log-group:/aws/lambda/processor:*"
      }
    ]
  })
}



resource "aws_iam_policy" "s3_processed_read_policy" {
  name        = "S3ReadPolicyForProcessed"
  description = "Policy for reading from Processed Bucket"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "s3:GetObject"
        ],
        Resource = "${aws_s3_bucket.processed_bucket.arn}/*"
      }
    ]
  })
}


resource "aws_iam_policy" "loader_logging_policy" {
  name        = "LoggingPolicyForLoader"
  description = "Policy for logging behaviour of Loader"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "logs:PutLogEvents",
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
        ],
        Resource = "arn:aws:logs:eu-west-2:144630460963:log-group:/aws/lambda/loader:*"
      }
    ]
  })
}


resource "aws_iam_policy" "secretsmanager_access" {
  name        = "SecretsManagerAccess"
  description = "Policy for accessing secretsmanager"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "secretsmanager:GetSecretValue"
        ],
        Resource = "*"
      }
    ]
  })
}


resource "aws_iam_role" "ingestor_lambda_role" {
  name = "IngestorLambdaRole"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "sts:AssumeRole"
        ],
        Principal = {
          Service = [
            "lambda.amazonaws.com"
          ]
        }
      }
    ]
  })
}

resource "aws_iam_policy_attachment" "ingestor_lambda_s3_policy_attachment" {
  name       = "IngestorLambdaRoleWritePolicyAttachment"
  roles      = [aws_iam_role.ingestor_lambda_role.name]
  policy_arn = aws_iam_policy.s3_ingested_write_policy.arn
}

resource "aws_iam_policy_attachment" "ingestor_lambda_history_logging_policy_attachment" {
  name       = "IngestorLambdaRoleHistoryLoggingPolicyAttachment"
  roles      = [aws_iam_role.ingestor_lambda_role.name]
  policy_arn = aws_iam_policy.ingestor_history_logging_policy.arn
}

resource "aws_iam_policy_attachment" "ingestor_lambda_logging_policy_attachment" {
  name       = "IngestorLambdaRoleLoggingPolicyAttachment"
  roles      = [aws_iam_role.ingestor_lambda_role.name]
  policy_arn = aws_iam_policy.ingestor_logging_policy.arn
}

resource "aws_iam_policy_attachment" "ingestor_lambda_secretsmanager_access_attachment" {
  name       = "IngestorLambdaRoleSecretsManagerAccessAttachment"
  roles      = [aws_iam_role.ingestor_lambda_role.name]
  policy_arn = aws_iam_policy.secretsmanager_access.arn
}

resource "aws_iam_role" "processor_lambda_role" {
  name = "ProcessorLambdaRole"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "sts:AssumeRole"
        ],
        Principal = {
          Service = [
            "lambda.amazonaws.com"
          ]
        }
      }
    ]
  })
}

resource "aws_iam_policy_attachment" "processor_lambda_s3_read_policy_attachment" {
  name       = "ProcessorLambdaRoleReadPolicyAttachment"
  roles      = [aws_iam_role.processor_lambda_role.name]
  policy_arn = aws_iam_policy.s3_ingested_read_policy.arn
}

resource "aws_iam_policy_attachment" "processor_lambda_s3_write_policy_attachment" {
  name       = "ProcessorLambdaRoleWritePolicyAttachment"
  roles      = [aws_iam_role.processor_lambda_role.name]
  policy_arn = aws_iam_policy.s3_processed_write_policy.arn
}

resource "aws_iam_policy_attachment" "processor_lambda_logging_policy_attachment" {
  name       = "ProcessorLambdaRoleLoggingPolicyAttachment"
  roles      = [aws_iam_role.processor_lambda_role.name]
  policy_arn = aws_iam_policy.processor_logging_policy.arn
}

resource "aws_iam_policy_attachment" "processor_lambda_secretsmanager_access_attachment" {
  name       = "ProcessorLambdaRoleSecretsManagerAccessAttachment"
  roles      = [aws_iam_role.processor_lambda_role.name]
  policy_arn = aws_iam_policy.secretsmanager_access.arn
}

resource "aws_iam_role" "loader_lambda_role" {
  name = "LoaderLambdaRole"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "sts:AssumeRole"
        ],
        Principal = {
          Service = [
            "lambda.amazonaws.com"
          ]
        }
      }
    ]
  })
}

resource "aws_iam_policy_attachment" "loader_lambda_s3_read_policy_attachment" {
  name       = "LoaderLambdaRoleReadPolicyAttachment"
  roles      = [aws_iam_role.loader_lambda_role.name]
  policy_arn = aws_iam_policy.s3_processed_read_policy.arn
}


resource "aws_iam_policy_attachment" "loader_lambda_secretsmanager_access_attachment" {
  name       = "LoaderLambdaRoleSecretsManagerAccessAttachment"
  roles      = [aws_iam_role.loader_lambda_role.name]
  policy_arn = aws_iam_policy.secretsmanager_access.arn
}


resource "aws_iam_policy_attachment" "loader_lambda_logging_policy_attachment" {
  name       = "LoaderLambdaRoleLoggingPolicyAttachment"
  roles      = [aws_iam_role.loader_lambda_role.name]
  policy_arn = aws_iam_policy.loader_logging_policy.arn
}
