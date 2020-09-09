data "aws_iam_policy_document" "secret_access" {
  statement {
    actions   = ["secretsmanager:GetSecretValue"]
    resources = ["*"]
    principals {
      identifiers = ["${aws_iam_role.assume_role.arn}"]
      type        = "AWS"
    }
  }
}


resource "aws_secretsmanager_secret" "app_config" {
  name = "app-config-${local.environment}"

  policy = data.aws_iam_policy_document.secret_access.json
}