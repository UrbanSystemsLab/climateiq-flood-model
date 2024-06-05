LOCATION=us-central1
JOB_NAME=

echo "LOCATION=${LOCATION}"
echo "JOB_NAME=${JOB_NAME}"

gcloud batch jobs delete "${JOB_NAME}" --location="${LOCATION}"