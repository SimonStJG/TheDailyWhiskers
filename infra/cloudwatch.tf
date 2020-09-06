locals {
  metric_name      = "ErrorCount"
  metric_namespace = "DailyWhiskers"
}

resource "aws_cloudwatch_event_rule" "daily_trigger" {
  name                = "dw-daily-trigger"
  schedule_expression = "cron(0 9 * * ? *))"
}

resource "aws_cloudwatch_event_target" "daily_trigger" {
  arn  = aws_lambda_function.service.arn
  rule = aws_cloudwatch_event_rule.daily_trigger.name
}

resource "aws_cloudwatch_log_group" "lambda" {
  # Name is determined by AWS, so must match the below
  name              = "/aws/lambda/${aws_lambda_function.service.function_name}"
  retention_in_days = 7
}

resource "aws_cloudwatch_log_metric_filter" "errors" {
  name           = "DailyWhiskersErrors"
  pattern        = "\"[ERROR]\""
  log_group_name = aws_cloudwatch_log_group.lambda.name

  metric_transformation {
    name          = local.metric_name
    namespace     = "DailyWhiskers"
    value         = "1"
    default_value = "0"
  }
}

resource "aws_cloudwatch_metric_alarm" "errors" {
  alarm_name          = "DailyWhiskersError"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name         = local.metric_name
  namespace           = local.metric_namespace
  period              = "300"
  threshold           = "0"
  alarm_actions       = [aws_sns_topic.error_notification.arn]
  statistic           = "Sum"
  datapoints_to_alarm = "1"
}
