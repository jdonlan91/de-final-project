resource "aws_s3_bucket" "ingested_bucket" {
  bucket_prefix       = "ingested-"
  object_lock_enabled = true
}

resource "aws_s3_bucket" "processed_bucket" {
  bucket_prefix       = "processed-"
  object_lock_enabled = true
}

resource "aws_s3_bucket_object_lock_configuration" "ingested_bucket_object_lock" {
  bucket = aws_s3_bucket.ingested_bucket.id

  rule {
    default_retention {
      mode = "GOVERNANCE"
      days = 30
    }
  }
}

resource "aws_s3_bucket_object_lock_configuration" "processed_bucket_object_lock" {
  bucket = aws_s3_bucket.processed_bucket.id

  rule {
    default_retention {
      mode = "GOVERNANCE"
      days = 30
    }
  }
}
