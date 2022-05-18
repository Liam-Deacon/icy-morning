# Icy Morning Project

![python](https://img.shields.io/static/v1?label=python&message=3.10&color=blue&logo=python) ![terraform](https://img.shields.io/static/v1?label=IaC&message=Terraform&color=purple&logo=terraform) ![aws](https://img.shields.io/static/v1?label=Cloud&message=AWS&color=orange&logo=amazon-aws) ![lambda](https://img.shields.io/static/v1?label=Serverless&message=Lambda&color=orange&logo=aws-lambda)

## Overview

Repository to showcase a cloud engineering project bringing together a simple FastAPI REST API app with database backing store using SQLAlchemy and targeting AWS infrastructure using Terraform.

The AWS infrastraucture is provisioned with Terraform for deploying the FastAPI Lambda function. It creates an API using an AWS API Gateway and Lambda function, based on [this walkthrough](https://towardsdatascience.com/fastapi-aws-robust-api-part-1-f67ae47390f9).  The setup uses:

- _REST API_: [FastAPI](https://fastapi.tiangolo.com/) and [Mangum](https://mangum.io/)
- _Infrastructure_: [Terraform](https://www.terraform.io/) and [Serverless](https://www.serverless.com/)

Requests are sent to the API Gateway, which handles all requests using a [proxy integration with the Lambda function](https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html). Mangum acts as a wrapper, which allows FastAPI to handle the requests and create responses the API gateway can serve. All logs are sent to CloudWatch log groups.

```js
          ┌─── AWS region ───────────────────────────────────┐
          │                  ┌─── VPC: 1..n AZs ──────────┐  │  
          │                  │  ┌──────────────────────┐  │  │ 
Request  ───►  API Gateway  ──────►  Lambda (FastAPI)  │  │  │ 
          │                  │  └────────────────│─────┘  │  │
          │                  │          ┌────────│───┐    │  │
          │                  │          │    RDS ▼   │    │  │
          │                  │          └────────────┘    │  │
          │         │        └───│────────────────────────┘  │
          │ ┌───────│────────────│─────┐                     │
          │ │       ▼ CloudWatch ▼     │                     │
          │ └──────────────────────────┘                     │
          └──────────────────────────────────────────────────┘
```

### Solution Notes

CloudWatch is not currently implemented.

If performance becomes an issue, a CloudFront distribution could be added for API responses that are cacheable (i.e. the READ operations), however the cache would need to be refreshed after each WRITE operation.

## Deployment

Start by navigating into the `infrastructure/` directory and performing the following commands:

```bash
cd infrastructure/
make create-deployment
```

For tearing down the deployment:

```bash
cd infrastructure/
make destroy-deployment
```

### Pre-requisites

#### Terraform

If you wish to create a terraform state that is shared between users/machines (e.g. in DevOps scenarios) then first create an s3 bucket [using this guide](https://www.golinuxcloud.com/configure-s3-bucket-as-terraform-backend/). Once done `make main.tf` can be used to guide the user into configuring the TF backend to use S3.

##### API Gateway Custom Domain

Place your `ca.crt`, `certificate.crt` and `certificate.key` files for your custom domain under `infrastructure/certs` and add an `infrastructure/overrides.tf` file containing values for the following variables:

- `api_gateway_domain`
- `api_gateway_certificate_name`

Finally do a `make api_gateway_custom_domain.tf` to add the configuration to Terraform. Remove with `make clean`.

> NOTE: This feature is currently untested.

## Development

Development is assumed to be in a Linux environment with the following tools available:

- bash
- pyenv (or python3.10)
- make
- terraform

If you are using Linux then the toolchain can be installed using `make install-dev`.

Assuming the aforementioned tools are installed and available on the system PATH,
then setting up the python virtual environment for development is as simple as
`make init`.

### Local Server

To start a local test server, do:

```bash
make serve
```

Provided the virtual environment has been initialised correctly, this will serve a local REST API under [http://127.0.0.1:8000](http://127.0.0.1:8000). The OpenAPI (Swagger) documentation is available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) and can be used to test endpoints with/without authentication.

### Testing

To run the API tests locally (after setting up the dev environment as described above):

```bash
make clean test  # clean is currently required due to async SQLite driver needing to point to a file.
```

## TODO:

- [ ] Implement SSO authentication with JWT
- [ ] Send an email notification / allow subscription to Asset creation events
- [ ] Use `alembic` for handling database migrations
- [ ] Add FastAPI exception handlers to handle different python errors intuitively.
- [ ] CI for terraform module validation and security checks
