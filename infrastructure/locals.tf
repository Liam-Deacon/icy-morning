locals {

  // This will be used for name and tagging all our resources
  tag_name = "${var.project_name}-${var.stage}"

  sso_secrets = jsondecode(
    data.aws_secretsmanager_secret_version.this.secret_string
  )

  use_custom_domain = var.route53_root_domain_name != ""

  rds_secrets = jsondecode(
    data.aws_secretsmanager_secret_version.rds_creds.secret_string
  )

  rds_admin_username = local.rds_secrets["username"]

  rds_admin_password = local.rds_secrets["password"]
}