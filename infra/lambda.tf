resource "aws_lambda_function" "service" {
  function_name = "dailywhiskers-${local.environment}"
  handler       = "dailywhiskers/dailywhiskers.handler"
  filename      = var.lambda_code_zip
  runtime       = "python3.6"
  role          = aws_iam_role.service.arn
  timeout       = 180                                   # 3 Minutes
}

resource "aws_lambda_permission" "daily_trigger" {
  statement_id_prefix = "AllowExecutionFromCloudwatch_"
  action              = "lambda:InvokeFunction"
  function_name       = aws_lambda_function.service.function_name
  principal           = "events.amazonaws.com"
  source_arn          = aws_cloudwatch_event_rule.daily_trigger.arn
  depends_on          = [aws_cloudwatch_log_group.lambda]
}
