### Data Engineering Challenge in GCP

#### Solution

The solution was developed based on the platform [Google Cloud Platform](https://cloud.google.com/).

#### Description of folders

- __terraform__:
Contains the terraform files responsible for creating all features of the GCP.

- __dataproc__:
Contains files related to the Dataproc workflow template.

- __composer__:
Contains the DAG file.

- __scripts__:
Contains utility bash scripts.

#### Instructions for running the code

__Note__: The steps described here were tested in the Ubuntu 20.04.

###### GCP Config

1. Create a new project in GCP and note its ID.
2. From the root folder, run:

```bash
./replace_project_id.sh YOUR_PROJECT_ID
```
this will replace a placeholder string in all files where the project ID is used.

3. Download and Install Cloud SDK, Instructions [here](https://cloud.google.com/sdk/docs/install).
4. Configure GCP authentication, instructions [here](https://cloud.google.com/docs/authentication/getting-started).

###### Terraform configuration

1. Download and install Terraform, instructions [here](https://learn.hashicorp.com/tutorials/terraform/install-cli).
2. run:
```bash
scripts/setup_terraform_backend.sh
```
which will create the storage range that serves as the back end to store the Terraform state.

3. in the directory __terraform__ , run:

```bash
terraform init && terraform apply
```
and type __yes__ when solicited. Wait for the process to complete, which can take up to 40 minutes.

###### Dataproc Workflow Template

1. From the root folder, run:
```bash
scripts/deploy_workflow_template.sh
```
to copy the python file to GCS and import the workflow template. After that, the template is ready to be used in the project.

###### Deploy DAG
1. In the composer folder, you can find the DAG file, upload it to your DAGs folder in Cloud Composer.

2. From the root folder, run:

```bash
scripts/upload_files.sh
```
which will upload the files to the bucket for processing.
obs: (In this case you will only upload the wordcount.txt file, as git does not upload heavy files, you will need to upload the file to the folder, locally, before running the bash script).


