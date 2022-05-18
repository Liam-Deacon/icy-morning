# Import the Secrets which got created recently and store it so that we can use later. 


data "aws_secretsmanager_secret" "icy_morning_rds_secrets" {
  arn = aws_secretsmanager_secret.icy_morning_rds_secrets.arn
}

data "aws_secretsmanager_secret_version" "icy_morning_rds_secrets_version" {
  secret_id = aws_secretsmanager_secret.icy_morning_rds_secrets.id
  depends_on = [
    aws_secretsmanager_secret.icy_morning_rds_secrets,
    aws_secretsmanager_secret_version.icy_morning_rds_secrets_version

  ]
}