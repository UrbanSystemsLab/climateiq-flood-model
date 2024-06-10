echo "LOCATION=${LOCATION}"
echo "JOB_NAME=${JOB_NAME}"

gcloud beta batch jobs submit "${JOB_NAME}-${LOCATION}" --location="${LOCATION}"  --config="jobs/${JOB_NAME}.json"