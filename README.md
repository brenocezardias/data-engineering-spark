### Teste para vaga de Engenheiro de dados na Luiza Labs

#### Solução

A solução foi desenvolvida com base na plataforma [Google Cloud Platform](https://cloud.google.com/).

#### Descrição das pastas

- __terraform__:
Contém os arquivos de terraform responsáveis por criar todos os recursos do GCP.

- __dataproc__:
Contém arquivos relacionados ao modelo de fluxo de trabalho do Dataproc.

- __composer__:
Contém o arquivo DAG.

- __scripts__:
Contém scripts de bash de utilitários.

#### Instruções para executar o código

__Note__: As etapas descritas aqui foram testadas no Ubuntu 20.04.

###### Configuração GCP

1. Crie um novo projeto no GCP e anote seu ID.
2. Na pasta raiz, execute:

```bash
./replace_project_id.sh YOUR_PROJECT_ID
```
isso substituirá uma string de espaço reservado em todos os arquivos onde o ID do projeto é usado.

3. Baixe e instale o Cloud SDK, instruções [aqui](https://cloud.google.com/sdk/docs/install).
4. Configure a autenticação do GCP, instruções [aqui](https://cloud.google.com/docs/authentication/getting-started).

###### Configuração do Terraform

1. Baixe e instale o Terraform, instruções [aqui](https://learn.hashicorp.com/tutorials/terraform/install-cli).
2. Execute:
```bash
scripts/setup_terraform_backend.sh
```
que criará o intervalo de armazenamento que serve como back-end para armazenar o estado do Terraform.

3. No diretório __terraform__ , execute:

```bash
terraform init && terraform apply
```
e digite __yes__ quando solicitado. Aguarde a conclusão do processo, o que pode levar até 40 minutos.

###### Dataproc Workflow Template
1. Da pasta raiz, execute:
```bash
scripts/deploy_workflow_template.sh
```
para copiar o arquivo python para o GCS e importar o modelo de fluxo de trabalho. Depois disso, o modelo está pronto para ser usado no projeto.

###### Implantar DAG
1. Na pasta composer, se encontra o arquivo da DAG, faça o upload para a sua pasta de DAGs no Cloud Composer.

2. Da pasta raiz, execute:

```bash
scripts/upload_files.sh
```
que irá fazer o upload dos arquivo no bucket, para processamento. 
obs: (Nesse caso irá fazer o upload apenas do arquivo wordcount.txt, pois o git não sobe arquivos pesados, será necessário fazer o upload do arquivo para a pasta, localmente, antes de executar o script bash).


