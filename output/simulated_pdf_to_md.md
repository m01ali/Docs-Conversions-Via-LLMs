```markdown
# RAG with Amazon Bedrock and OpenSearch

Opinionated sample on how to configure and deploy [RAG (Retrieval Augmented Generation)](https://research.ibm.com/blog/retrieval-augmented-generation-RAG) application.

It is comprised of a few core pieces:

- [Amazon Bedrock](https://aws.amazon.com/bedrock/) as the managed service providing easy API-based access to [foundation models (FMs)](https://aws.amazon.com/what-is/foundation-models/).
  
- [Amazon OpenSearch Service](https://aws.amazon.com/opensearch-service/). This is an open-source alternative to using [Amazon Kendra](https://aws.amazon.com/kendra/).

- [LangChain](https://www.langchain.com/) as a [Large Language Model (LLM)](https://www.elastic.co/what-is/large-language-models) application framework. It has also been used to update the OpenSearch index when new documents get added to the knowledgebase S3 bucket.

- [Amazon Elastic Container Service (ECS)](https://aws.amazon.com/ecs/) to run the RAG Application.

- [Streamlit](https://streamlit.io/) for the frontend user interface of the RAG Application.

- [Application Load Balancer](https://aws.amazon.com/elasticloadbalancing/application-load-balancer/) to route HTTPS traffic to the ECS service (which is running the RAG App).

- [Amazon Cognito](https://aws.amazon.com/cognito/) for secure user authentication.

This sample is inspired by [another sample](https://github.com/aws-samples/rag-with-amazon-bedrock-and-pgvector) that demonstrates similar functionality with PGVector (instead of OpenSearch).

## Architecture

![Architecture](./architecture/arch_aoss_rag.png)

## Short note on vector data stores

A [Vector database](https://en.wikipedia.org/wiki/Vector_database) is an essential component of any RAG application. The LLM framework uses the vector data store to search for information based on the user’s queries.

The typical assumption (*and a strong constraint on this sample project*) is that a knowledgebase would comprise of PDF documents stored somewhere. Ideally, a true knowledgebase would encompass a lot more—scrape websites, wiki pages, and so on. But to limit the scope of this sample, the knowledgebase is an [S3](https://aws.amazon.com/s3/) bucket containing a bunch of PDF documents.

A popular choice for a vector database in an AWS-based RAG app is Amazon Kendra. It does [optical character recognition (OCR)](https://en.wikipedia.org/wiki/Optical_character_recognition) for PDFs under the hood. It is a fully managed search service with seamless integration with AWS Services like S3. Additionally, Amazon Bedrock also has a vector database offering in the form of ["Knowledgebases"](https://aws.amazon.com/bedrock/knowledge-bases/).

**Note** - "Bedrock Knowledgebases" is another vector store offering; and **it should not** be confused with the term "knowledgebase" and/or "knowledgebase bucket" which refers to the S3 bucket containing PDF documents in this project.

However, the purpose of this sample was to show how to set up an open-source vector database, and since Kendra and Bedrock Knowledgebases are not open source, this sample focuses on OpenSearch. Unlike Kendra, OpenSearch cannot directly query PDF documents, so we need to extract the text, and then feed the text to OpenSearch.

## OpenSearch orchestration

* The expectation is that PDF files will land in the knowledgebase S3 bucket—either by manually uploading them via the console, or programmatically via the [AWS CLI](https://aws.amazon.com/cli/) or by running `cdk deploy BaseInfraStack`.
  
  **Note** - the last option (*`cdk deploy`*) requires that you put the PDF files in the ["knowledgebase"](./knowledgebase/) directory of this project. The [S3 Bucket Deployment](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_s3_deployment.BucketDeployment.html) construct will then upload these files to the knowledgebase bucket.

* Once the files land in the knowledgebase S3 bucket, [S3 Event Notifications](https://docs.aws.amazon.com/AmazonS3/latest/userguide/EventNotifications.html) initiate a [lambda](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html) function to extract text from the PDF file(s), and upload the converted text files into the "processed text S3 Bucket". The code/logic for this conversion [lambda function](./lambda/pdf-processor/lambda_function.py) is in the [lambda/pdf-processor](./lambda/pdf-processor/) directory. The function uses the [pypdf](https://github.com/py-pdf/pypdf) Python Library to achieve the text extraction.

* After the processed text files land in the "processed text S3 bucket", another S3 Event Notification triggers another lambda function ([aoss-trigger](./lambda/aoss-trigger/app.py)) that extracts the necessary information about the file and pushes it off to an [Amazon SQS](https://aws.amazon.com/sqs/) queue.

* That message push in the SQS initiates another lambda function ([aoss-update](./lambda/aoss-update/app.py)) that finally updates the vector database with the contents of the processed text file to be indexed (*which will enable it to be searched by the RAG app*). It uses the [S3FileLoader](https://python.langchain.com/docs/integrations/document_loaders/aws_s3_file) component from LangChain to extract document contents to feed OpenSearch.

### Short note on Embeddings

[Embeddings](https://www.elastic.co/what-is/vector-embedding) are a way to convert words and sentences into numbers that capture their meaning and relationships. In the context of RAG, these "vector embeddings" aid in ["similarity search"](https://en.wikipedia.org/wiki/Similarity_search) capabilities. Adding documents to an OpenSearch index also requires the creation/provisioning of embeddings. This project/sample has utilized [OpenAI's Embeddings](https://platform.openai.com/docs/guides/embeddings). So, if you wish to build/run this app in your AWS environment, you will need to create an account with OpenAI and need their [API Key](https://help.openai.com/en/articles/4936850-where-do-i-find-my-api-key).

**OpenAI has its own pricing on its API usage** so be mindful of that. You can find that out on their [pricing page](https://openai.com/pricing). You should be able to get going with the free credits, but if you keep this app running long enough, it will start accruing additional charges.

Some other options to obtain embeddings:

- [HuggingFace](https://huggingface.co/blog/getting-started-with-embeddings)
  
- [Amazon Titan](https://aws.amazon.com/about-aws/whats-new/2023/09/amazon-titan-embeddings-generally-available/)

**Note** - If you wish to use alternative embeddings, you will need to change the code in the [rag-app](./rag-app/) and the [aoss-update lambda function](./lambda/aoss-update/) accordingly.

## Deploying the app

This project is divided into a few sub-stacks, so deploying it also requires a few additional steps. It uses [AWS CDK](https://aws.amazon.com/cdk/) for [Infrastructure as Code (IaC)](https://en.wikipedia.org/wiki/Infrastructure_as_code).

### Pre-requisites

- Since this is a [TypeScript](https://www.typescriptlang.org/) CDK project, you should have [npm](https://www.npmjs.com/) installed (which is the package manager for TypeScript/JavaScript).
  
  - You can find installation instructions for npm [here](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm).

- Install [AWS CLI](https://aws.amazon.com/cli/) on your computer (*if not already done so*).
  
  ```bash
  pip install awscli
  ```
  
  This means you need to have Python installed on your computer (if it is not already installed).
  
  - You need to also configure and authenticate your AWS CLI to be able to interact with AWS programmatically. Detailed instructions of how you could do that are provided [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html).

- You need to have [docker](https://www.docker.com/) installed on your computer.
  
  - You can check out these options for building and running docker containers on your local machine:
    
    - [Docker desktop](https://www.docker.com/products/docker-desktop/): Most popular container management app. Note - it does require a license if the organization you work for is bigger than a certain threshold.
    
    - [Rancher desktop](https://rancherdesktop.io/): A popular open-source container management tool.
    
    - [Finch](https://github.com/runfinch/finch): Another open-source tool for container management. Note - currently it only supports MacOS machines.

- Have an API Key from [OpenAI](https://openai.com/). This key is needed for programmatic access to use their embeddings for OpenSearch. You need to create an account with OpenAI (*if you don't already have one*). Details to find/create an API Key can be found [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-api-key).

### Create a self-signed SSL certificate

- Set the `IAM_SELF_SIGNED_SERVER_CERT_NAME` environment variable. This is the name of the self-signed server certificate that will be created ([via IAM](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_server-certs.html)) as part of the deployment.
  
  ```bash
  export IAM_SELF_SIGNED_SERVER_CERT_NAME=<name you want to give to your ssl cert>
  ```

- Run the [self-signed-cert-utility.py](./scripts/self-signed-cert-utility/self-signed-cert-utility.py) script in the [scripts](./scripts/) directory to create a self-signed certificate, and upload its contents to AWS via `boto3` API calls.

This is needed because the Application Load Balancer requires [SSL certificates](https://www.cloudflare.com/en-gb/learning/ssl/what-is-an-ssl-certificate/) to have a functioning [HTTPS listener](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/create-https-listener.html).

```bash
# switch to the self-signed-cert-utility directory
cd scripts/self-signed-cert-utility

# create a python3 virtual environment (highly recommended)
python3 -m virtualenv .certenv

# activate the virtual environment
source .certenv/bin/activate
# for a different shell like fish, just add a `.fish` at the end of the previous command

# install requirements
pip install -r requirements.txt

# run the script
python self-signed-cert-utility.py
# optionally specify a `--profile` if you're not using the default AWS profile

# deactivate virtual environment
deactivate

# return to the root directory of the project
cd -
```

If the script runs successfully, you should see a JSON-like object printed out in the log output with parameters like `ServerCertificateName`, `ServerCertificateId`, `Arn` etc. Moreover, the `HTTPStatusCode` should have the value `200`.

The parameters encoded in the certificate are in a JSON file. By default, it expects a file named ["default_cert_parameters.json"](./scripts/self-signed-cert-utility/default_cert_params.json) unless otherwise specified. You may change the values of the default JSON file if you wish to. If you wish to use your configuration file (*instead of the default*), you can do so by specifying the `--config-file` parameter.

You can also specify a custom domain for the certificate by setting the `APP_DOMAIN` environment variable.

**Note** - an alternative would be to use the [AWS Certificates Manager](https://aws.amazon.com/certificate-manager/) but it requires additional steps (*in the form of creating and registering your domain, involving [Route53 hosted zones](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/hosted-zones-working-with.html) etc.*). And since the focus of this sample is to show the deployment of a RAG app, and not registering domains etc., it does not delve into configuring that bit.

### Define the domain name for the Cognito hosted UI [Optional]

Set the `COGNITO_DOMAIN_NAME` environment variable. This will be the domain of the [Cognito hosted UI](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-app-integration.html) used to "log-in" and/or "sign-up" into the app.

```bash
export COGNITO_DOMAIN_NAME=<name you want to give to your cognito hosted ui domain>
```

The default value is defined in the [base-infra-stack.ts](./lib/base-infra-stack.ts#L260).

### Install dependencies (if not already done)

```bash
npm install
```

### Bootstrap CDK environment (if not already done)

Bootstrapping provisions resources in your environment such as an Amazon Simple Storage Service (Amazon S3) bucket for storing files and AWS Identity and Access Management (IAM) roles that grant permissions needed to perform deployments. These resources get provisioned in an AWS CloudFormation stack, called the bootstrap stack. It is usually named CDKToolkit. Like any AWS CloudFormation stack, it will appear in the AWS CloudFormation console of your environment once it has been deployed. More details can be found [here](https://docs.aws.amazon.com/cdk/v2/guide/bootstrapping.html).

```bash
npx cdk bootstrap

# You can optionally specify `--profile` at the end of that command if you wish to not use the default AWS profile.
```

**Note** - you only need to do this once per account. If there are other CDK projects deployed in your AWS account, you won't need to do this.

### Set environment variable (if you are on an M1/M2 Mac)

Depending on the architecture of your computer, you may need to set this environment variable for the docker container. This is because docker containers depend on the architecture of the host machine that is building/running them.

**If your machine runs on the [x86](https://en.wikipedia.org/wiki/X86) architecture, you can ignore this step.**

```bash
export DOCKER_CONTAINER_PLATFORM_ARCH=arm
```

### Deploy the BaseInfraStack

```bash
npx cdk deploy BaseInfraStack

# You can optionally specify `--profile` at the end of that command if you wish to not use the default AWS profile.
```

This will deploy the base infrastructure - consisting of a VPC, Application Load Balancer for the app, S3 buckets (for knowledgebase, and processed text), Lambda functions to process the PDF documents, some SQS queues for decoupling, a Secret credential for the OpenAI API key, Cognito user pool, and some more bits and pieces of the cloud infrastructure. The CDK code for this is in the [lib](./lib) directory within the [base-infra-stack.ts](./lib/base-infra-stack.ts) file.

### Upload the OpenAI API key to Secrets Manager

The secret was created after the deployment of the `BaseInfraStack` but the value inside it is not valid. You can either enter your OpenAI API key via the AWS Secrets Manager console; Or you could use the [api-key-secret-manager-upload.py](./scripts/api-key-secret-manager-upload/api-key-secret-manager-upload.py) script to do that for you.

[AWS Secrets Manager](https://aws.amazon.com/secrets-manager/) is the recommended way to store credentials in AWS, as it provides API-based access to credentials for databases, etc. Since OpenAI (*the provider we are using the vector embeddings from*) is an external service and has its own API keys, we need to manually upload that key to Secrets Manager so that the app infrastructure can access it securely.

```bash
# switch to the api-key-secret-manager-upload directory
cd scripts/api-key-secret-manager-upload

# create a python3 virtual environment (highly recommended)
python3 -m virtualenv .keyenv

# activate the virtual environment
source .keyenv/bin/activate
# for a different shell like fish, just add a `.fish` at the end of the previous command

# install requirements
pip install -r requirements.txt

# run the script; optionally specify a `--profile` if you're not using the default AWS profile
python api-key-secret-manager-upload.py -s openAiApiKey

2024-01-14 19:42:59,341 INFO  [__main__]:[MainThread] AWS Profile being used: default
2024-01-14 19:42:59,421 INFO  [__main__]:[MainThread] Updating Secret: openAiApiKey
Please enter the API Key:
2024-01-14 19:44:02,221 INFO  [__main__]:[MainThread] Successfully updated secret value
2024-01-14 19:44:02,221 INFO  [__main__]:[MainThread] Total time elapsed: 62.88090920448303 seconds
# deactivate virtual environment
deactivate

# return to the root directory of the project
cd -
```

The script will prompt you to enter your OpenAI API key. It uses the [getpass](https://docs.python.org/3/library/getpass.html) Python library so that you don't have to enter it in plain text.

**Note** - that the instructions specify `-s openAiApiKey`. It is the same name as defined in the [base-infra-stack.ts](./lib/base-infra-stack.ts?plain=1#L124). If you change the value there, you will need to change the value whilst running the script too.

### Deploy the TestCompute Stack

```bash
npx cdk deploy TestComputeStack

# You can optionally specify `--profile` at the end of that command if you wish to not use the default AWS profile.
```

This will deploy an EC2 instance that you may use to troubleshoot OpenSearch connectivity/make API calls, etc., and/or any other test/dev computing you might need to do.

### Deploy the OpenSearch stack

```bash
npx cdk deploy OpenSearchStack

# You can optionally specify `--profile` at the end of that command if you wish to not use the default AWS profile.
```

This will deploy an [Amazon managed OpenSearch serverless collection](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-overview.html#serverless-start) - specialized to do Vector Searches. The reason to use this is so that you don't have to worry about managing the OpenSearch cluster. Additionally, it will create and attach some [network security policies](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-network.html), [encryption security policies](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-encryption.html) and [data access policies](https