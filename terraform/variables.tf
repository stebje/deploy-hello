variable "aws_region" {
  description = "AWS region to deploy the infrastructure"
  default     = "us-west-1"
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  default     = "10.0.0.0/16"
}

variable "db_username" {
  description = "Database username"
  default     = "postgres"
}

variable "db_password" {
  description = "Database password"
  default     = "YourSecurePassword"
}

variable "db_name" {
  description = "Database name"
  default     = "postgres"
}
