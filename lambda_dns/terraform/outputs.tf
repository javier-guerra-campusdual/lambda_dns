output "lambda_function_arn" {
  description = "ARN de la función Lambda"
  value       = aws_lambda_function.dns_updater.arn
}

output "lambda_function_name" {
  description = "Nombre de la función Lambda"
  value       = aws_lambda_function.dns_updater.function_name
}

output "lambda_role_arn" {
  description = "ARN del rol IAM de la función Lambda"
  value       = aws_iam_role.lambda_role.arn
}

output "eventbridge_rule_arn" {
  description = "ARN de la regla EventBridge"
  value       = aws_cloudwatch_event_rule.ec2_state_change.arn
}

output "cloudwatch_log_group" {
  description = "Nombre del grupo de logs en CloudWatch"
  value       = "/aws/lambda/${aws_lambda_function.dns_updater.function_name}"
}