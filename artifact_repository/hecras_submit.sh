LOCATION="us-central1"
REPOSITORY="hecras-repository"

gcloud builds submit --region=${LOCATION} --tag ${LOCATION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY}/hecras-image:latest