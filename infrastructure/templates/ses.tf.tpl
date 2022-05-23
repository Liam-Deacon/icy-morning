# NOTE: needs configuration of target domain records, see https://technotrampoline.com/articles/configuring-spf-dkim-and-dmarc-for-aws-ses-with-terraform/
data "aws_route53_zone" "main" {
  name         = var.hosted_zone_domain
  private_zone = false
}

resource "aws_ses_domain_identity" "ses_domain" {
  domain = var.ses_domain
}

resource "aws_ses_domain_mail_from" "main" {
  domain           = aws_ses_domain_identity.ses_domain.domain
  mail_from_domain = "mail.${var.ses_domain}"
}

resource "aws_route53_record" "amazonses_verification_record" {
  zone_id = data.aws_route53_zone.main.zone_id
  name    = "_amazonses.${var.ses_domain}"
  type    = "TXT"
  ttl     = "600"
  records = [join("", aws_ses_domain_identity.ses_domain.*.verification_token)]
}

resource "aws_ses_domain_dkim" "ses_domain_dkim" {
  domain = join("", aws_ses_domain_identity.ses_domain.*.domain)
}

resource "aws_route53_record" "amazonses_dkim_record" {
  count   = 3
  zone_id = data.aws_route53_zone.main.zone_id 
  name    = "${element(aws_ses_domain_dkim.ses_domain_dkim.dkim_tokens, count.index)}._domainkey.${var.ses_domain}"
  type    = "CNAME"
  ttl     = "600"
  records = ["${element(aws_ses_domain_dkim.ses_domain_dkim.dkim_tokens, count.index)}.dkim.amazonses.com"]
}

resource "aws_route53_record" "spf_mail_from" {
  zone_id = data.aws_route53_zone.main.zone_id 
  name    = aws_ses_domain_mail_from.main.mail_from_domain
  type    = "TXT"
  ttl     = "600"
  records = ["v=spf1 include:amazonses.com -all"]
}

resource "aws_route53_record" "spf_domain" {
  zone_id = data.aws_route53_zone.main.zone_id   
  name    = var.ses_domain
  type    = "TXT"
  ttl     = "600"
  records = ["v=spf1 include:amazonses.com -all"]
}
