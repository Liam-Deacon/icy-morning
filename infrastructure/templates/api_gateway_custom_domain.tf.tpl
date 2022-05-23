resource "null_resource" "custom_api_gateway_domain_enabled" {
  count = (var.api_gateway_domain == "") ? 1 : 0
}

resource "aws_api_gateway_domain_name" "domain" {
  domain_name = var.api_gateway_domain

  certificate_name        = var.api_gateway_certificate_name
  certificate_body        = "${file("${path.module}/certs/${var.api_gateway_certificate_filename}")}"
  certificate_chain       = "${file("${path.module}/certs/${var.api_gateway_certificate_ca_filename}")}"
  certificate_private_key = "${file("${path.module}/certs/${var.api_gateway_certificate_key_filename}")}"

  depends_on = [
    null_resource.custom_api_gateway_domain_enabled
  ]
}


resource "aws_api_gateway_base_path_mapping" "base_path_mapping" {
  api_id      = "${aws_apigatewayv2_api.api.id}"
  
  domain_name = "${aws_api_gateway_domain_name.domain.domain_name}"

  depends_on = [
    null_resource.custom_api_gateway_domain_enabled,
    aws_api_gateway_domain_name.domain 
  ]
}