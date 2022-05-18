output "lambda_bucket_name" {
  description = "Name of the S3 bucket used to store function code."
  value = aws_s3_bucket.lambda_bucket.id
}

output "api_endpoint" {
  description = "Link to the REST API."
  value = aws_apigatewayv2_api.api.api_endpoint
}

output "rds_instance_endpoint" {
  description = "The connection endpoint in address:port format"
  value       = aws_db_instance.rds.endpoint
}

output "rds_instance_address" {
  description = "The hostname of the RDS instance"
  value       = aws_db_instance.rds.address
}

output "rds_instance_port" {
  description = "The database port"
  value       = aws_db_instance.rds.port
}

output "database_name" {
  description = "Name of the database"
  value       = aws_db_instance.rds.name
}

output "database_username" {
  description = "Database Username"
  value       = aws_db_instance.rds.username
  sensitive   = true
}

output "database_password" {
  description = "Database Password"
  value       = aws_db_instance.rds.password
  sensitive   = true
}