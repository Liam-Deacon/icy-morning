#! /bin/bash

S3_BUCKET_NAME="${S3_BUCKET_NAME:-}"

echo "Configuring S3 backend with Terraform state..."

read -p "S3 bucket name [\"${S3_BUCKET_NAME}\"]: " bucket_name
bucket_name="${bucket_name:-$S3_BUCKET_NAME}"
if [[ -z "$bucket_name" ]]; then
    echo "No S3 bucket given, skipping configuration..." 1>&2
    exit 1
fi

read -p "AWS region [\"${AWS_REGION}\"]: " aws_region
aws_region="${aws_region:-$AWS_REGION}"
if [[ -z "$aws_region" ]]; then
    echo "No AWS region given, skipping configuration..." 1>&2
    exit 1
fi

read -p "DynamoDB table name [\"${DYAMODB_TABLE_NAME}\"]: " dynamodb_table_name
dynamodb_table_name="${dynamodb_table_name:-$DYNAMODB_TABLE_NAME}"
if [[ -z "$dynamodb_table_name" ]]; then
    echo "No DynamoDB table name given, skipping configuration..." 1>&2
    exit 1
fi

# Generates terraform backend config based on user input
cat >main.tf <<EOF
terraform { 
  backend "s3" { 
    bucket         = "$bucket_name" 
    key            = "terraform.tfstate" 
    region         = "$aws_region" 
    dynamodb_table = "$dynamodb_table_name" 
  } 
} 
EOF