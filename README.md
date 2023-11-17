## Data Engineering Final Project - Team Basalt (Stian)

### Contributors

- Christopher Johnston ([GitHub](https://github.com/CJohnston079), [LinkedIn](http://www.linkedin.com/in/christopher-johnston-122221219))
- Iuliia Kostina ([GitHub](https://github.com/IuliaKostina), [LinkedIn](http://linkedin.com/in/iuliia-kostina))
- Joseph Donlan ([GitHub](https://github.com/jdonlan91), [LinkedIn](https://www.linkedin.com/in/joedonlanphd/))
- Santhy Tamang ([GitHub](https://github.com/santhyt), [LinkedIn](https://www.linkedin.com/in/santhy-tamang-1280071a/))

with advice and support from:

- Danika Crawley
- Joe Mulvey

### Overview

Welcome to the repo for the final project of Team Basalt - completed across three weeks in Q4 2023 as part of the Data Engineering Bootcamp at Northcoders.

A full brief can be found in the [Project Specification](/readme_files/ProjectSpecification.md) - here is a brief summary.

**Background**

Our goal in this project was to deliver an end-to-end cloud-based data platform for a hypothetical retail client that sells designer tote bags.

The client currently collects and stores data on various aspects of its operations in an online transactional processing (OLTP) database, and would like to have this data processed automatically into a data lakehouse to make it more amenable to analysis.

The solution we built:

1. extracts data at regular intervals from the client's OLTP database.
2. transforms the data into a star schema, storing it in a file-based data lake.
3. loads the data into the client's online analytics processing (OLAP) database.

All components of this system are hosted in the cloud on Amazon Web Services.

### Implementation

Here is a visual overview of the data pipeline, highlighting the flow of data through the pipeline, and the AWS services used for each component:

![A visual overview of the data pipeline](/readme_files/PipelineDiagram.png "Data Pipeline - Team Basalt")

The core of our pipeline consists of three Lambda functions. Each of these functions is written in Python, with code that is checked for security vulnerabilities and PEP-8 compliance, as well as unit-tested with a test coverage of 99%. All Lambda functions and separate utils functions have docstrings which describe their arguments, return values and behaviour in detail.

1. The ingestor function fetches all newly updated data from the source database, converts this to .csv format, and deposits this data in AWS S3 'ingested' bucket. It is triggered by an EventBridge event every 5 minutes.

The ingestor keeps a log of its ingestion history: on the first invocation it fetches all data from the source database; on subsequent invocations it fetches only data which has been added to the database since the previous invocation.

2. The processor function transforms the data from .csv to .parquet format. It is triggered upon deposition of a .csv file in the ingested S3 bucket, and applies the appropriate transformation function to reformat the data from the source table to match the star schema of the destination warehouse. It then converts the remodelled data to .parquet format and deposits it into a 'processed' bucket, which acts as the data lake.

3. The loader function populates the destination data warehouse with data from the .parquet files. It fetches newly added .parquet files from the processed S3 bucket, reads the data from these files and then loads the data into the warehouse.

Like the ingester, the loader is triggered at 5-minute intervals and tracks its invocation history. On the first invocation it fetches all files from processed bucket and also seeds the dim_date database with entries for every day in a 3-year range; on subsequent invocations it loads only data from .parquet files which arrived in the processed bucket since the previous invocation.

We deployed all of our AWS infrastructure via an Infrastructure-As-Code approach using Terraform. This allowed us to reproducibly deploy the infrastructure, ensure all the components correctly referenced each other, and are deployed in the correct order. We stored the Terraform state information and other back-end files in a separately deployed S3 bucket, and database credentials were stored securely in AWS Secrets Manager.

To ensure our pipeline continues to run stably and that it successfully processes data that continually arrives in the source data warehouse, we set up a robust monitoring and alerting process. All lambda functions have detailed AWS Cloudwatch logs of their behaviour and we created metrics to track different types of errors for the three lambdas. If errors occur they trigger custom Cloudwatch alarms linked to AWS SNS topics which allow us to receive immediate email notifications.

### Installation and Deployment

**To install and run the code.**

1. Create and activate a virtual environment.

```bash
python -m venv venv
source venv/bin/activate
```

2. Install Make (if not already installed)

On Linux:

```bash
sudo apt install make -y
```

On Mac, via [Homebrew](https://brew.sh/)

```bash
brew install make
```

3. Install the dependencies.

```bash
make requirements
```

3. Set up the development environment.

```bash
make dev-setup
```

4. Run security checks (uses the safety and bandit libraries).

```bash
make security-test
```

5. Check that the code is PEP8 compliant (uses the flake8 library).

```bash
make run-flake
```

6. Run the unit tests.

```bash
flake8  ./src/*/*.py ./test/*.py
```

7. Check the test coverage.

```bash
make check-coverage
```

Note: steps 4-7 can be run in a single step using

```bash
make run-checks
```

To deploy the pipeline you need credentials for PostgreSQL [source](https://dbdiagram.io/d/6332fecf7b3d2034ffcaaa92) and [destination](https://dbdiagram.io/d/637a423fc9abfc611173f637) data warehouses matching the linked schema.

You also need an AWS account or IAM user with admin privileges. Create secrets in AWS Secrets Manager containing the two sets of database credentials - these secrets must be named 'totesys_db_credentials' (source) and 'postgres_db_credentials' (destination).

**Deploying the pipeline via GitHub Actions**

This project contains a test-and-deploy.yml file which allows the data pipeline to be deployed automatically via a CI-CD pipeline run via GitHub actions. The test and deploy workflow runs all the checks described in the previous section and then deploys all of the AWS infrastructure using Terraform.

1. Add the credentials for your AWS admin privileges account (under the names AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY) to [GitHub secrets](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions).

2. Run the CI/CD pipeline by pushing your code to any branch on the remote repo.

**Deploying the pipeline locally**

Alternatively you can deploy the pipeline by executing commands on your local machine.

1. Add the credentials for your AWS admin privileges account (under the names AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY) to a plaintext file called credentials in a folder called .aws in your home directory.

If you already use Terraform on your machine, skip to 4.

2. Install the AWS command-line-interface tool (instructions [here](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html))

3. Install Terraform (instructions [here](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli))

4. Initialise Terraform in the tf directory.

```bash
cd tf
terraform init
```

5. See Terraform's plan for the cloud infrastructure it will build.

```bash
terraform plan
```

6. Build the infrastructure.

```bash
terraform apply
```

(you will need to answer 'yes' when prompted to confirm that Terraform should proceed)
