resource "aws_lambda_function" "icy_morning_lambda" {
  # NOTE: build filename with `make icy-morning-fast-api.zip` under infrastucture/ directory
  filename      = "../dist/icy-morning-fast-api.zip"  # TODO: consider using s3 archive instead
  function_name = "icy-morning"
  role          = aws_iam_role.test_role.arn
  handler       = "app.api.main_app.handler"
  runtime       = "python3.8"  # NOTE: terraform validate fails with 3.9+

  # reserved_concurrent_executions = var.lambda_reserved_concurrent_operations  # set to minimum for aws account


  environment {
    variables = {
      AUTH_TYPE           = local.api_auth_type
      BASIC_AUTH_USERNAME = var.basic_auth_username
      BASIC_AUTH_PASSWORD = var.basic_auth_password

      SQLALCHEMY_DATABASE_CONNECTION_URI = "postgresql+asyncpg://${local.rds_admin_username}:${local.rds_admin_password}@${aws_db_instance.rds.address}:${aws_db_instance.rds.port}/${aws_db_instance.rds.name}"
    }
  }
}

# HTTP API
resource "aws_apigatewayv2_api" "api" {
    name          = "icy-morning-api"
    protocol_type = "HTTP"
    target        = aws_lambda_function.icy_morning_lambda.arn 
}

# Permission
resource "aws_lambda_permission" "apigw" {
	action        = "lambda:InvokeFunction"
	function_name = aws_lambda_function.icy_morning_lambda.arn
	principal     = "apigateway.amazonaws.com"

	source_arn = "${aws_apigatewayv2_api.api.execution_arn}/*/*"
}


data "aws_secretsmanager_secret_version" "rds_creds" {
  # write your secret name here
  secret_id = aws_secretsmanager_secret.this.id
}