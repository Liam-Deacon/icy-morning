data "aws_route53_zone" "root_domain" {
  name         = "${var.route53_root_domain_name}"
  private_zone = false
}

resource "null_resource" "route53_enabled" {
    count = var.use_custom_domain ? 1 : 0
}

# The domain name to use with api-gateway
resource "aws_api_gateway_domain_name" "domain_name" {
  domain_name = "${var.route53_sub_domain_name}"

  certificate_arn = "${aws_acm_certificate.cert.arn}"

  depends_on = [
    null_resource.route53_enabled
  ]
}

resource "aws_route53_record" "sub_domain" {
  name    = "${var.route53_sub_domain_name}"
  type    = "A"
  zone_id = "${data.aws_route53_zone.root_domain.zone_id}"

  alias {
    name                   = "${aws_api_gateway_domain_name.domain_name.cloudfront_domain_name}"
    zone_id                = "${aws_api_gateway_domain_name.domain_name.cloudfront_zone_id}"
    evaluate_target_health = false
  }

  depends_on = [
    null_resource.route53_enabled
  ]
}

resource "aws_acm_certificate" "cert" {
  # api-gateway / cloudfront certificates need to use the us-east-1 region
  provider          = "aws.cloudfront-acm-certs"
  domain_name       = "${var.route53_sub_domain_name}"
  validation_method = "DNS"

  depends_on = [
    null_resource.route53_enabled
  ]
}

resource "aws_route53_record" "cert_validation" {
  name    = "${aws_acm_certificate.cert.domain_validation_options.0.resource_record_name}"
  type    = "${aws_acm_certificate.cert.domain_validation_options.0.resource_record_type}"
  zone_id = "${data.aws_route53_zone.root_domain.zone_id}"
  records = ["${aws_acm_certificate.cert.domain_validation_options.0.resource_record_value}"]
  ttl     = 60

  depends_on = [
    null_resource.route53_enabled
  ]
}

resource "aws_acm_certificate_validation" "cert" {
  # api-gateway / cloudfront certificates need to use the us-east-1 region
  provider          = "aws.cloudfront-acm-certs"

  certificate_arn         = "${aws_acm_certificate.cert.arn}"
  validation_record_fqdns = ["${aws_route53_record.cert_validation.fqdn}"]

  timeouts {
    create = "45m"
  }

  depends_on = [
    null_resource.route53_enabled
  ]
}