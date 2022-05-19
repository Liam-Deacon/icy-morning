# Import the Secrets which got created recently and store it so that we can use later. 


data "aws_secretsmanager_secret" "icy_morning_rds_secret" {
  arn = aws_secretsmanager_secret.icy_morning_rds_secret.arn
}

data "aws_secretsmanager_secret_version" "icy_morning_rds_secret_version" {
  secret_id = aws_secretsmanager_secret.icy_morning_rds_secret.id
  depends_on = [
    aws_secretsmanager_secret.icy_morning_rds_secret,
    aws_secretsmanager_secret_version.icy_morning_rds_secret_version

  ]
}