resource "random_pet" "lambda_bucket_name" {
  prefix = "icy-morning-fast-api-func"
  length = 4
}

# This is the bucket where the lambda will be stored.
resource "aws_s3_bucket" "lambda_bucket" {
  bucket = random_pet.lambda_bucket_name.id
  acl           = "private"
  force_destroy = true
}