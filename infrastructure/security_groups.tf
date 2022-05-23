resource "aws_default_security_group" "default" {
  vpc_id = aws_vpc.main.id
}

resource "aws_security_group" "lambda" {
  vpc_id = aws_vpc.main.id
  name   = "${local.tag_name}-lambda-sg"

  description = "Allow outbound traffic from lambda"

  egress {
    description = "Outbound"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "rds" {
  vpc_id = aws_vpc.main.id
  name   = "${local.tag_name}-rds-sg"
  
  description = "Allow inbound traffic to postgres server"

  ingress {
    description     = "PostgreSQL"
    from_port       = 5432
    protocol        = "tcp"
    to_port         = 5432
    security_groups = [aws_security_group.lambda.id]  #, aws_security_group.ssh.id]
  }

  egress {
    description = "Outbound"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# TODO: consider removing unneeded SSH code
# resource "null_resource" "ssh_enabled" {
#   count = var.ec2_ssh_tunnel_enabled ? 1 : 0
# }
#
# resource "aws_security_group" "ssh" {
#   vpc_id = aws_vpc.main.id
#   name   = "${local.tag_name}-bastion-sg"
#
#   ingress {
#     from_port   = 22
#     to_port     = 22
#     protocol    = "tcp"
#     cidr_blocks = ["0.0.0.0/0"]
#   }
#
#   egress {
#     from_port   = 0
#     to_port     = 0
#     protocol    = "-1"
#     cidr_blocks = ["0.0.0.0/0"]
#   }
#
#   depends_on = [
#     null_resource.ssh_enabled
#   ]
# }

output "lambda_sg_id" {
  value = aws_security_group.lambda.id
}