terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = var.aws_region
}

# Create S3 bucket
resource "aws_s3_bucket" "fx_bucket" {
  bucket        = var.s3_bucket
  force_destroy = true # will delete contents of bucket when we run terraform destroy
}