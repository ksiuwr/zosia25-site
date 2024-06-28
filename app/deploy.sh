#!/bin/sh
set -eu

PROJECT_ID="<put Google Cloud Project ID here>"
REPO_NAME=zosia-repo
REGION=europe-central2
REPO_HOSTNAME=$REGION-docker.pkg.dev
IMAGE_NAME=zosia_prod

IMAGE_URL=$REPO_HOSTNAME/$PROJECT_ID/$REPO_NAME/$IMAGE_NAME:latest

# Configure gcloud and docker to be able to push to the Google Container Registry
gcloud config set project $PROJECT_ID
gcloud auth configure-docker $REPO_HOSTNAME

# Build and push the image
docker build --target prod -t $IMAGE_URL .
docker push $IMAGE_URL

# Run the migration job
gcloud run jobs execute migrate --wait --region=$REGION

# Run the collectstatic job which will collect all the static files into GCS bucket
gcloud run jobs execute collectstatic --wait --region=$REGION

# Deploy new service revision with the new image
gcloud run services update zosia --region $REGION --image $IMAGE_URL
