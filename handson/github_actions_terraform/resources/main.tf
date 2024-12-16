provider "aws" {}

variable "project" {
  type = string
}

variable "stage" {
  type = string
}

resource "aws_ssm_parameter" "test_param" {
  name  = "/${var.project}/${var.stage}/test_param"
  type  = "String"
  value = "test_value"
}
