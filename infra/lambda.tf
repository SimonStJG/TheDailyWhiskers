resource "aws_lambda_function" "service" {
  function_name = "dailywhiskers-${local.environment}"
  handler       = "thedailywhiskers/dailywhiskers.handler"
  filename      = var.lambda_code_zip
  runtime       = "python3.6"
  role          = aws_iam_role.assume_role.arn
  timeout       = 180 # 3 Minutes

  environment {
    variables = {
      REGION_NAME = data.aws_region.current.name
      SECRET_NAME = aws_secretsmanager_secret.app_config.name
    }
  }
}

resource "aws_lambda_permission" "daily_trigger" {
  statement_id_prefix = "AllowExecutionFromCloudwatch_"
  action              = "lambda:InvokeFunction"
  function_name       = aws_lambda_function.service.function_name
  principal           = "events.amazonaws.com"
  source_arn          = aws_cloudwatch_event_rule.daily_trigger.arn
  depends_on          = [aws_cloudwatch_log_group.lambda]
}
