# provides a container registry for the API
resource "aws_ecr_repository" "api_ecr" {
  name = "icy-morning-api-repository"
  image_tag_mutability = "IMMUTABLE"
  encryption_configuration {
    encryption_type = "KMS"
  }
  image_scanning_configuration {
    scan_on_push = true
  }
}