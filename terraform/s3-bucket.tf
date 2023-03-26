# Create S3 bucket
resource "aws_s3_bucket" "s3_bucket" {
  bucket = var.s3_bucket
}

# Set access control of bucket to private
resource "aws_s3_bucket_acl" "s3_reddit_bucket_acl" {
  bucket = aws_s3_bucket.s3_bucket.id
  acl    = "private"
}