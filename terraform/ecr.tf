provider "aws" {
  region = var.aws_region
}

resource "aws_ecr_repository" "api_service_repo" {
  name = "api-service-repo2"

  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecr_repository" "backend_service_repo" {
  name = "backend-service-repo2"

  image_scanning_configuration {
    scan_on_push = true
  }
}
