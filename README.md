# deploy-hello

## Description

This repo can be used to deploy the necessary infrastructure and source code to AWS to expose a public endpoint that will return a string when called over `http`, e.g. a `curl` command. See below for details.

The source code is deployed using Docker to Elastic Container Registry, and run on Elastic Container Service with Fargate (serverless). All infrastructure is deployed using terraform.

## Pre-requisites

- [Docker](https://docs.docker.com/desktop/)
- [Terraform](https://developer.hashicorp.com/terraform/install?product_intent=terraform)
- [AWS CLI](https://aws.amazon.com/cli/)

```sh
$ terraform version && docker version && aws --version

Terraform v1.9.6
(...)
Client:
 Version:           27.2.0
(...)
aws-cli/2.17.61 Python/3.12.6 Darwin/23.5.0 source/x86_64
```

## Usage

### Configuration

```sh
git clone https://github.com/stebje/deploy-hello.git
```

- Ensure that you are authenticated with AWS in the CLI

```sh
aws sts get-caller-identity
```

- If you are not yet authenticated, run the command below and follow the instructions [here](https://docs.aws.amazon.com/cli/latest/reference/configure/)

```sh
aws configure
```

- Rename `.env.sample` --> `.env`
- Update `.env` with your AWS account ID, preferred AWS region, and the names of your ECR repos
    - :warning: The ECR repo names must match what is configured in `terraform/ecr.tf`

> [!TIP]
> You can get your AWS account ID using the AWS CLI:
> `aws sts get-caller-identity --query "Account" --output text`

```env
AWS_ACCOUNT_ID=12345678
AWS_REGION=us-west-1
API_REPO_NAME=api-service-repo2
DB_REPO_NAME=backend-service-repo2
```

### Deployment



### Test

## Structure

```
.
├── README.md
├── docker_auth_build_push.sh
├── api_service
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
├── backend_service
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
└── terraform
    ├── ecr.tf
    ├── main.tf
    ├── tfplan
    └── variables.tf
```

## Examples

...

## Troubleshooting

...
