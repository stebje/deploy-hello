#!/bin/bash

# Load environment variables from .env file
set -a
source .env
set +a

# Exit script on any command failure
set -e

# Access the environment variables
echo "--- Environment Variables ---"
echo "AWS Account ID: $AWS_ACCOUNT_ID"
echo "AWS Region: $AWS_REGION"
echo "ECR repo name - database: $DB_REPO_NAME"
echo "ECR repo name - api: $API_REPO_NAME"
echo "---"
echo ""

# Set dir location to bash script location
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "DIR: $DIR"

# Some convenience vars to reuse
ECR_URL="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"
DB_REPO="$ECR_URL/$DB_REPO_NAME"
API_REPO="$ECR_URL/$API_REPO_NAME"

# Authenticate docker with AWS ECR
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# Build and push docker containers to AWS ECR, label it latest
cd "$DIR"/backend_service
docker build --no-cache -t backend-service . || { echo "DB service build failed"; exit 1; }
docker tag backend-service:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$DB_REPO_NAME:latest
docker push $DB_REPO:latest

cd "$DIR"/api_service
docker build --no-cache -t api-service . || { echo "API service build failed"; exit 1; }
docker tag api-service:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$API_REPO_NAME:latest
docker push $API_REPO:latest