import os
import datetime

from airflow import models
from airflow.providers.google.cloud.operators.dataproc import (
    DataprocInstantiateWorkflowTemplateOperator,
)
from airflow.operators.dummy_operator import DummyOperator

DEFAULT_DAG_ARGS = {
    "owner": "Breno",
    "start_date": datetime.datetime(2021, 5, 14),
}

PROJECT_ID = "YOUR_PROJECT_ID"
ARTIFACTS_BUCKET = f"{PROJECT_ID}-spark-py"
WORDS_FILE = "gs://YOUR_PROJECT_ID-spark-files/clientes_pedidos.csv"
CUSTOMER_FILE = "gs://YOUR_PROJECT_ID-spark-files/wordcount.txt"

with models.DAG(
    dag_id="Spark_Process_Files", default_args=DEFAULT_DAG_ARGS, schedule_interval=None
) as dag:

    begin_dag = DummyOperator(task_id="begin-dag")

    process_logs = DataprocInstantiateWorkflowTemplateOperator(
        task_id="process-files",
        template_id="spark-process",
        project_id="YOUR_PROJECT_ID",
        region="us-central1",
        parameters={
            "CLUSTER_NAME": "process-spark-test",
            "MAIN_PY": f"gs://{ARTIFACTS_BUCKET}/dataproc-templates/spark_job.py",
            "WORDS_FILE": WORDS_FILE,
            "CUSTOMER_FILE": CUSTOMER_FILE,
        },
    )

    end_dag = DummyOperator(task_id="end-dag")

    begin_dag >> process_logs >> end_dag
