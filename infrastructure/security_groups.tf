resource "aws_security_group" "lambda" {
  vpc_id = aws_vpc.main.id
  name   = "${local.tag_name}-lambda-sg"

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "rds" {
  vpc_id = aws_vpc.main.id
  name   = "${local.tag_name}-rds-sg"
  ingress {
    description     = "PostgreSQL"
    from_port       = 5432
    protocol        = "tcp"
    to_port         = 5432
    security_groups = [aws_security_group.lambda.id, aws_security_group.ssh.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "null_resource" "ssh_enabled" {
  count = var.ec2_ssh_tunnel_enabled ? 1 : 0
}

resource "aws_security_group" "ssh" {
  vpc_id = aws_vpc.main.id
  name   = "${local.tag_name}-bastion-sg"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  depends_on = [
    null_resource.ssh_enabled
  ]
}

output "lambda_sg_id" {
  value = aws_security_group.lambda.id
}