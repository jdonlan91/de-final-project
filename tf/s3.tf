resource "aws_s3_bucket" "ingested_bucket" {
  bucket_prefix       = "ingested-"
}

resource "aws_s3_bucket" "processed_bucket" {
  bucket_prefix       = "processed-"
}


resource "aws_s3_bucket_notification" "ingested_bucket_notification" {
  bucket = aws_s3_bucket.ingested_bucket.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.processor.arn
    events              = ["s3:ObjectCreated:*"]
  }

  depends_on = [aws_lambda_permission.allow_s3_ingested_to_invoke_processor]
}