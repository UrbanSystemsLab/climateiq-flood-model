LOCATION="us-central1"
REPOSITORY="hecras-repository"

# Create the repository
gcloud artifacts repositories create ${REPOSITORY} \
    --repository-format=docker \
    --location=${LOCATION} \
    --description="Store the hecras docker image" \
    --async