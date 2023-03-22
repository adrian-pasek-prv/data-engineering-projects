variable "s3_bucket" {
  description = "Bucket name for S3"
  type        = string
  default     = ""
}

variable "aws_region" {
  description = "Region for AWS"
  type        = string
  default     = "eu-central-1"
}