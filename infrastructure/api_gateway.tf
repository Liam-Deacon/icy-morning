resource "aws_lambda_function" "icy_morning_lambda" {
  # NOTE: build filename with `make icy-morning-fast-api.zip` under infrastucture/ directory
  filename      = "../dist/icy-morning-fast-api.zip"  # TODO: consider using s3 archive instead
  function_name = "icy-morning"
  role          = aws_iam_role.test_role.arn
  handler       = "app.api.main_app.handler"
  runtime       = "python3.9"
  environment {
    variables = {
      AUTH_TYPE           = var.api_auth_type
      BASIC_AUTH_USERNAME = var.basic_auth_username
      BASIC_AUTH_PASSWORD = var.basic_auth_password
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
