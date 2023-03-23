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

# Set access control of bucket to private
resource "aws_s3_bucket_acl" "s3_fx_bucket_acl" {
  bucket = aws_s3_bucket.fx_bucket.id
  acl    = "private"
}