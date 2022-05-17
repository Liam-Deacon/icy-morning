resource "aws_cloudwatch_dashboard" "CloudWatchDashboard" {
  dashboard_name = "Icy-Morning-Dashboard"

  # TODO: Add widgets for dashboard
  dashboard_body = <<EOF
{
    "widgets": [
    ]
}
EOF
}