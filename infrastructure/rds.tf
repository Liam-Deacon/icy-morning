# create RDS SQL SERVER db instance
resource "aws_db_instance" "rds" {
  count                         = var.db_enabled ? 1 : 0
  allocated_storage             = var.db_allocated_storage
  allow_major_version_upgrade   = var.db_allow_major_version_upgrade
  auto_minor_version_upgrade    = var.db_auto_minor_version_upgrade
  max_allocated_storage         = var.db_max_allocated_storage
  maintenance_window            = var.db_maintenance_window
  monitoring_interval           = var.db_monitoring_interval
  backup_retention_period       = var.db_backup_retention_period
  backup_window                 = var.db_backup_window
  deletion_protection           = var.db_deletion_protection
  db_subnet_group_name          = aws_db_subnet_group.rds.*.id[0]
  character_set_name            = var.db_character_set_name
  engine                        = var.db_engine 
  engine_version                = var.db_engine_version
  identifier                    = var.db_identifier
  instance_class                = var.db_instance_class
  username                      = local.sso_secrets.username
  password                      = local.sso_secrets.password
  skip_final_snapshot           = var.db_skip_final_snapshot
  storage_encrypted             = var.db_storage_encrypted
  # storage_type                = var.storage_type
  vpc_security_group_ids        = var.vpc_security_group_ids
  publicly_accessible           = var.db_publicly_accessible
  apply_immediately             = var.db_apply_immediately
  license_model                 = var.db_license_model
  port                          = var.db_port
  parameter_group_name          = var.db_parameter_group_name
  performance_insights_enabled  = var.db_performance_insights_enabled
  tags                          = var.tags
  multi_az                      = var.db_multi_az
  timezone                      = var.db_timezone
  final_snapshot_identifier     = var.db_final_snapshot_identifier_prefix

  depends_on = [
    aws_db_subnet_group.rds,
    aws_secretsmanager_secret.this,
    aws_secretsmanager_secret_version.this

  ]
}

# create db subnet group
resource "aws_db_subnet_group" "rds" {
  count                         = var.db_enabled ? 1 : 0
  name                          = "${var.db_identifier}-subnet-group"
  description                   = "Created by terraform"
  subnet_ids                    = var.subnet_ids
  tags                          = var.tags
}


#  create a random generated password which we will use in secrets.
resource "random_password" "password" {
  length                        = 12
  special                       = true
  min_special                   = 2
  override_special              = "_%"
}


# create secret and secret versions for database master account 
resource "aws_secretsmanager_secret" "this" {
  name                          = var.secret_manager_name
  recovery_window_in_days       = 7
  tags                          = var.tags
}

resource "aws_secretsmanager_secret_version" "this" {
  secret_id                     = aws_secretsmanager_secret.this.id
  secret_string = <<EOF
   {
    "username": "admin",
    "password": "${random_password.password.result}"
   }
EOF
}