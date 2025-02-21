provider "aws" {
  region = var.aws_region
}

# Lambda Function
resource "aws_lambda_function" "dns_updater" {
  filename         = var.lambda_zip_path
  function_name    = "dns-updater"
  role            = aws_iam_role.lambda_role.arn
  handler         = "handler.lambda_handler"
  runtime         = "python3.9"
  timeout         = 30

  environment {
    variables = {
      HOSTED_ZONE_ID = var.hosted_zone_id
      DOMAIN_SUFFIX  = var.domain_suffix
    }
  }
}

# EventBridge Rule
resource "aws_cloudwatch_event_rule" "ec2_state_change" {
  name        = "capture-ec2-state-change"
  description = "Captura cambios de estado en instancias EC2"

  event_pattern = jsonencode({
    source      = ["aws.ec2"]
    detail-type = ["EC2 Instance State-change Notification"]
    detail = {
      state = ["running"]
    }
  })
}

# EventBridge Target
resource "aws_cloudwatch_event_target" "lambda" {
  rule      = aws_cloudwatch_event_rule.ec2_state_change.name
  target_id = "SendToLambda"
  arn       = aws_lambda_function.dns_updater.arn
}

# Lambda Permission
resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowEventBridgeInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.dns_updater.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.ec2_state_change.arn
}