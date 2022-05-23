// grab the availability zones for the region we set in var.tf
data "aws_availability_zones" "available" {
  state = "available"
}

resource "aws_vpc" "main" {
  # checkov:skip=CKV2_AWS_11:TODO: Ensure VPC flow logging is enabled in all VPCs
  cidr_block           = var.cidr_block_vpc
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    name = local.tag_name
  }
}

resource "aws_subnet" "public" {
  # checkov:skip=CKV_AWS_130:TODO: Resolve "Ensure VPC subnets do not assign public IP by default"
  cidr_block              = var.cidr_block_subnet_public
  vpc_id                  = aws_vpc.main.id
  availability_zone       = "${var.aws_region}a"  # data.aws_availability_zones.available.names[0]
  map_public_ip_on_launch = true
  tags = {
    name = "${local.tag_name}-public"
  }
}

// RDS cluster in serverless mode requires at least 3 AZs

resource "aws_subnet" "private" {
  count = length(var.cidr_block_subnets_private)
  // name  = "${local.tag_name}-private-${count.index}"

  cidr_block        = var.cidr_block_subnets_private[count.index]
  vpc_id            = aws_vpc.main.id
  availability_zone = "${var.aws_region}b"  # data.aws_availability_zones.available.names[count.index]
  tags = {
    name = "${local.tag_name}-private-${count.index}"
  }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  tags = {
    name = local.tag_name
  }
}

// NAT gateway requires an elastic ip
resource "aws_eip" "public" {
  # checkov:skip=CKV2_AWS_19:FIXME: Ensure that all EIP addresses allocated to a VPC are attached to EC2 instances

  tags = {
    name = local.tag_name
  }
}

resource "aws_nat_gateway" "main" {
  allocation_id = aws_eip.public.id
  // connect to public subnet
  subnet_id = aws_subnet.public.id
  tags = {
    name = local.tag_name
  }
}

# Track IP traffic logs
# resource "aws_flow_log" "aws_vpc_log" {
#   iam_role_arn    = aws_iam_role.lambda_role.arn  # FIXME: change to dedicated role
#   # log_destination = "log"
#   traffic_type    = "ALL"
#   vpc_id          = aws_vpc.main.id
# }

// Output the subnet ids which will be used in the serverless.yml later
output "subnet_private" {
  value = tolist(aws_subnet.private.*.id)
}