resource "random_pet" "sqs_queue_name" {
  prefix = "icy-morning-sqs_queue"
  length = 3
}

resource "aws_sqs_queue" "icy_morning_sqs" {
  name = random_pet.sqs_queue_name.id

  # checkov:skip=CKV_AWS_27:FIXME: Ensure all data stored in the SQS queue is encrypted
#   kms_master_key_id                 = "alias/aws/sqs"
#   kms_data_key_reuse_period_seconds = 300
}

resource "aws_sqs_queue_policy" "icy_morning_sqs_policy" {
  queue_url = aws_sqs_queue.icy_morning_sqs.id

  policy = <<POLICY

  "Version": "2012-10-17",
  "Id": "sqspolicy",
  "Statement": [
    
      "Sid": "First",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "sqs:SendMessage",
      "Resource": "${aws_sqs_queue.icy_morning_sqs.arn}"
    
  ]
POLICY
}