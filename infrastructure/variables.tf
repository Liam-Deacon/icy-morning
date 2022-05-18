variable "aws_region" {
  description = "AWS region for all resources."
  type    = string
  default = "eu-west-2"  # e.g. In the UK use London if there are any data export concerns 
}

variable "allowed_hosts" {
  description = "Separated list of allowed hosts"
  default     = "*"
}

variable "archive_root" {
  type = string
  default = "./../dist"
}

variable "api_name" {
  type = string
  default = "icy-morning"
}

variable "password" {
  description = "RDS Password"
  type        = string
  default     = ""
}

variable "secret_id" {
  description = "secret id"
  type        = string
  default     = ""
}

variable "vpc_security_group_ids" {
  description = "List of VPC security groups to associate"
  type        = list(string)
  default     = []
}

variable "db_enabled" {
  default     = true
  description = "Set to `false` to prevent the module from creating any resources"
  type        = bool
}

variable "db_skip_final_snapshot" {
  default     = true
  description = "Set to `false` to skip_final_snapshot"
  type        = bool
}
variable "db_storage_encrypted" {
  default     = true
  description = "Set to `false` to not encrypt the storage"
  type        = bool
}
variable "db_publicly_accessible" {
  default     = false
  description = "Set to `false` to prevent Database accessibility"
  type        = bool
}
variable "db_deletion_protection" {
  default     = true
  description = "Set to `false` to prevent database from deletation"
  type        = bool
}

variable "db_apply_immediately" {
  default     = true
  description = "Set to `false` to prevent immediate changes"
  type        = bool
}
variable "db_allocated_storage" {
  default     = "10"
  description = "Allocate storage size"
  type        = string
}

variable "db_backup_retention_period" {
  default     = "14"
  description = "enable auto backup and retention"
  type        = string
}
variable "db_subnet_group_name" {
  default     = ""
  description = "Specify db subnet group"
  type        = string
}
variable "db_engine" {
  default     = "postgres"
  description = "Specify engin name"
  type        = string
}
variable "db_identifier" {
  default     = "icy-morning-rds"
  description = "Specify DB name"
  type        = string
}

variable "db_engine_version" {
  default     = "14.1"
  description = "Specify DB version"
  type        = string
}
variable "db_instance_class" {
  default     = "db.t4g.micro"
  description = "Specify instance type"
  type        = string
}

variable "tags" {
  default     = {}
  description = "A map of tags to add to all resources"
  type        = map(string)
}

variable "subnet_ids" {
  type        = list(string)
  description = "List of subnets"
  default     = []

}

variable "secret_manager_name" {
  type = string
  description = " secret manager name"
  default = "secret_manager"
  
}

 variable "db_max_allocated_storage" {
  type = string 
  description = "Max allocate storage"
  default = null
  
 } 
#  variable "family" {
#   default = "sqlserver-se-15.0"
  
# }
 variable "db_license_model" {
  description = "One of license-included, bring-your-own-license, general-public-license, postgresql-license"
  default = "postgresql-license"
}

variable "db_port" {
  description = "The port on which to accept connections"
  type = string
  default = "5432"
}

variable "db_character_set_name" {
  description = "SQL Server collation to use"
  type = string
  default = "SQL_Latin1_General_CP1_CI_AS"
}

variable "db_parameter_group_name" {
  default = "rds-pg14-param-group"
}


variable "db_multi_az" {
  description = "Whether to have multiple availability zones for the RDS database"
  type        = bool
  default     = false
}

variable "db_timezone" {
  description = "The RDS database timezone"
  default     = "UTC"
}

variable "db_backup_window" {
  description = "When to perform DB backups"
  type        = string
  default     = "02:00-03:00"
}

variable "db_maintenance_window" {
  description = "When to perform DB maintenance"
  type = string
  default = "sun:05:00-sun:06:00"
}

variable "db_allow_major_version_upgrade" {
  default = false
}

variable "db_final_snapshot_identifier_prefix" {
  description = "The prefix name to use when creating a final snapshot on cluster destroy, appends a random 8 digits to name to ensure it's unique too."
  type        = string
  default     = "final"
}

variable "db_auto_minor_version_upgrade" {
  default = true
}

variable "db_performance_insights_enabled" {
  description = "Specifies whether Performance Insights is enabled or not."
  type        = bool
  default     = false
}

variable "db_create_monitoring_role" {
  description = "Whether to create the IAM role for RDS enhanced monitoring"
  type        = bool
  default     = false
}

variable "db_monitoring_interval" {
  description = "The interval (seconds) between points when Enhanced Monitoring metrics are collected"
  type        = number
  default     = 0
}

variable "ec2_ssh_tunnel_enabled" {
  type    = bool
  default = false
}

# NOTE: the following are automatically obtained from user environment variables

# variable "aws_access_key_id" {  # from $AWS_ACCESS_KEY_ID
#   type      = string
#   sensitive = true
# }

# variable "aws_access_secret_key" {  # from $AWS_SECRET_ACCESS_KEY
#   type      = string
#   sensitive = true
  
# }

variable project_name {
  default     = "serverless-rds-internet"
  description = "The base name of the project"
}

variable stage {
  description = "The development stage, like 'dev' or 'production'"
  default     = "dev"
}

variable db_name {
  description = "The database name"
  default     = "icy_morning"
}

variable db_username {
  description = "The database root username"
  default     = "postgres"
}

variable "cidr_block_vpc" {
  default = "10.1.0.0/16"
}

variable "cidr_block_subnet_public" {
  default = "10.1.1.0/24"
}
variable "cidr_block_subnets_private" {
  default = ["10.1.2.0/24", "10.1.3.0/24", "10.1.4.0/24"]
}

variable "bastion_host_key_pair_name" {
  default = "profile_eu_west_2"
}

variable "use_custom_domain" {
  description = "Whether to use a custom domain with AWS API Gateway v2"
  type        = bool
  default     = false
}

variable "route53_root_domain_name" {
  description = "The root domain for DNS lookup"
  default     = ""
}

variable "route53_sub_domain_name" {
  description = "The subdomain for the lambda app"
  default     = ""
}

variable "api_auth_type" {
  description = "The type of authentication to use for REST API, e.g. basic, jwt. NOTE: only 'basic' authentication is currently supported."
  default     = ""
}

variable "basic_auth_username" {
  description = "Username for REST API when using basic auth"
}

variable "basic_auth_password" {
  description = "Password for REST API when using basic auth"
}

variable "use_cloudwatch" {
  description = "Whether to use Amazon CloudWatch to monitor resources and applications in AWS"
  type        = bool
  default     = false 
}

variable "api_gateway_domain" {
  description = "Use a custom domain for API Gateway when populated"
  default = ""
}

variable "api_gateway_certificate_ca_filename" {
  description = "CA certificate filename for API gateway custom domain"
  default = "ca.crt"
}

variable "api_gateway_certificate_filename" {
  description = "CRT certificate filename for API gateway custom domain"
  default = "certificate.crt" 
}

variable "api_gateway_certificate_key_filename" {
  description = "KEY certificate filename for API gateway custom domain"
  default = "certificate.key"
}

variable "api_gateway_certificate_name" {
  description = "Certificate name for API gateway custom domain"
  default = ""
}

variable "lambda_reserved_concurrent_operations" {
  description = "The number of reserved concurrent operations for the Lambda. Cannot be less than that set on the AWS account."
  type = number
  default = -1
}