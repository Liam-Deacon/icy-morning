resource "aws_lambda_function" "icy_morning_lambda" {
  # NOTE: build filename with `make icy-morning-fast-api.zip` under infrastucture/ directory
  filename      = "../dist/icy-morning-fast-api.zip"  # TODO: consider using s3 archive instead
  function_name = "icy-morning"
  role          = aws_iam_role.test_role.arn
  handler       = "app.api.main_app.handler"
  runtime       = "python3.8"  # NOTE: terraform validate fails with 3.9+

  reserved_concurrent_executions = 2

  environment {
    variables = {
      AUTH_TYPE           = var.api_auth_type
      BASIC_AUTH_USERNAME = var.basic_auth_username
      BASIC_AUTH_PASSWORD = var.basic_auth_password

      SQLALCHEMY_DATABASE_CONNECTION_URI = "postgresql://${local.rds_admin_username}:${local.rds_admin_password}@${aws_db_instance.rds.address}:${aws_db_instance.rds.port}/${aws_db_instance.rds.name}"
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


resource "null_resource" "custom_api_gateway_domain_enabled" {
  count = (var.api_gateway_domain == "") ? 1 : 0
}

resource "aws_api_gateway_domain_name" "domain" {
  domain_name = var.api_gateway_domain

  certificate_name        = var.api_gateway_certificate_name
  certificate_body        = "${file("${path.module}/certs/${var.api_gateway_certificate_filename}")}"
  certificate_chain       = "${file("${path.module}/certs/${var.api_gateway_certificate_ca_filename}")}"
  certificate_private_key = "${file("${path.module}/certs/${var.api_gateway_certificate_key_filename}")}"

  depends_on = [
    null_resource.custom_api_gateway_domain_enabled
  ]
}


resource "aws_api_gateway_base_path_mapping" "base_path_mapping" {
  api_id      = "${aws_apigatewayv2_api.api.id}"
  
  domain_name = "${aws_api_gateway_domain_name.domain.domain_name}"

  depends_on = [
    aws_api_gateway_domain_name.domain 
  ]
}

data "aws_secretsmanager_secret_version" "rds_creds" {
  # write your secret name here
  secret_id = aws_secretsmanager_secret.this.id
}