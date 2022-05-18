resource "random_pet" "lambda_bucket_name" {
  prefix = "icy-morning-fast-api-func"
  length = 4
}

# This is the bucket where the lambda will be stored.
resource "aws_s3_bucket" "lambda_bucket" {
  bucket        = random_pet.lambda_bucket_name.id
  acl           = "private"
  force_destroy = true

  # checkov:skip=CKV_AWS_144:Cross region replication is not needed for testing
  # checkov:skip=CKV_AWS_145:TODO: Ensure that S3 buckets are encrypted with KMS by default

  versioning {
    enabled = true
  }


  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  # checkov:skip=CKV_AWS_18:TODO: configure bucket to log to
  # logging {
  # #   target_bucket = var.target_bucket
  # #   target_prefix = "log/${var.s3_bucket_name}"
  # }
}

resource "aws_s3_bucket_public_access_block" "lambda_bucket_public_access" {
  bucket = aws_s3_bucket.lambda_bucket.id

  restrict_public_buckets = true
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
}

