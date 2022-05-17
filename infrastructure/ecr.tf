# provides a container registry for the API
resource "aws_ecr_repository" "api_ecr" {
  name = "icy-morning-api-repository"
}