cd dataproc
PROJECT_ID="YOUR_PROJECT_ID"
REGION="us-central1"
BUCKET_NAME="YOUR_PROJECT_ID-spark-py"

TEMPLATE_FILE="spark_job.yaml"
TEMPLATE_NAME="spark-process"
PY_FILES_BUCKET=gs://$BUCKET_NAME/dataproc-templates/
PY_FILE="spark_job.py"

gsutil cp $PY_FILE $PY_FILES_BUCKET
yes | gcloud dataproc workflow-templates import $TEMPLATE_NAME \
    --project=$PROJECT_ID \
    --region=$REGION \
    --source=$TEMPLATE_FILE
