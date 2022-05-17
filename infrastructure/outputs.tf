output "lambda_bucket_name" {
  description = "Name of the S3 bucket used to store function code."
  value = aws_s3_bucket.lambda_bucket.id
}

output "api_endpoint" {
  description = "Link to the REST API."
  value = aws_apigatewayv2_api.api.api_endpoint
}
