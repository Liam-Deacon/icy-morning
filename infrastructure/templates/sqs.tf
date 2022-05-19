resource "random_pet" "sqs_queue_name" {
  prefix = "icy-morning-sqs_queue"
  length = 3
}

resource "aws_sqs_queue" "icy_morning_sqs" {
  name = random_pet.sqs_queue_name.id
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