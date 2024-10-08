# deploy-hello

## Description

This repo can be used to deploy the necessary infrastructure and source code to AWS to expose a public endpoint that will return a string when called over `http`, e.g. a `curl` command. See below for details.

The source code is deployed using Docker to Elastic Container Registry, and run on Elastic Container Service with Fargate (serverless). All infrastructure is deployed using terraform.

## Pre-requisites

- [Docker](https://docs.docker.com/desktop/)
- [Terraform](https://developer.hashicorp.com/terraform/install?product_intent=terraform)
- [AWS CLI](https://aws.amazon.com/cli/)

```sh
$ docker version && terraform version && aws --version

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
    - :warning: The AWS region in `.env` must match what is configured in `terraform/variables.tf`
    - :warning: The ECR repo names in `.env` must match what is configured in `terraform/ecr.tf`

> [!TIP]
> You can get your AWS account ID using the AWS CLI:
> 
> `aws sts get-caller-identity --query "Account" --output text`

```env
AWS_ACCOUNT_ID=12345678
AWS_REGION=us-west-1
API_REPO_NAME=api-service-repo2
DB_REPO_NAME=backend-service-repo2
```

### Deployment

- Ensure that the `API_REPO_NAME` and `DB_REPO_NAME` match the names configured in `terraform/ecr.tf`
- Create the ECR repositories

```sh
cd terraform
terraform init
terraform apply -target=aws_ecr_repository.api_service_repo -target=aws_ecr_repository.backend_service_repo
```

- Authenticate Docker with ECR and build/push the container images

```sh
cd ..
sh docker_auth_build_push.sh
```

- Deploy the remaining resources (⌛ *~5-10 minutes*)

```sh
cd terraform
terraform init
terraform plan -out=tfplan
terraform apply "tfplan"
```

### Test

- Once the `terraform` deployment is complete, fetch your load balancer DNS name and run a `curl` command against it

```sh
$ aws elbv2 describe-load-balancers --names app-alb --query 'LoadBalancers[0].DNSName' --region <AWS_REGION> --output text

$ curl http://<YOUT_LB_DNS>/messages/greeting
```

- Example

```sh
$ aws elbv2 describe-load-balancers --names app-alb --query 'LoadBalancers[0].DNSName' --region us-west-1 --output text
app-alb-1546875458.us-west-1.elb.amazonaws.com

$ curl http://app-alb-1546875458.us-west-1.elb.amazonaws.com/messages/greeting
{"message":"Hello World"}
```

> [!NOTE]
> Be aware that some resources such as the ECR tasks might take some time to spin up and register. If the test does not succeed directly after provisioning the resources then try again in a few mintues.

### Deprovison resources

- Once test is completed you can deprovision the AWS resources

```sh
terraform destroy
```

- Input `yes` when prompted and ensure that the deprovisioning is successful to avoid any unnecessary cost

### Troubleshooting

- The `terraform` provisions CloudWatch log groups that can be used to inspect the logs from the API service and the backend/database service
- Some resources exist in a global namespace such as IAM roles. If you encounter errors relating to the IAM role already existing then you can import the role with terraform before re-running `terraform plan ...` and `terraform apply ...`. Example:

```sh
cd terraform
terraform import aws_iam_role.ecs_execution_role ecs-execution-role2
```

- Secrets that are *scheduled* for deletion but not yet deleted will interfer with the provisioning of a new secret with the same name. If an error message relates to this during `terraform apply ...` then the secrets can be manually deleted before re-running `terraform plan ...` and `terraform apply ...`

```sh
$ aws secretsmanager list-secrets --region <AWS_REGION> --include-planned-deletion

$ aws secretsmanager delete-secret --secret-id <SECRET_NAME> --region us-west-2 --force-delete-without-recovery
```