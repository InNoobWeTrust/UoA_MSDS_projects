#!/usr/bin/env bash

# s3fs-fuse is an open-source project that allows to mount an S3 bucket to a local file storage
sudo apt update -y
sudo apt install -y docker.io
sudo snap install aws-cli --classic

# Download docker image
aws s3 --no-sign-request cp s3://{{S3_BUCKET}}/docker-registry/ad-rec-flask.tar .

# Load docker images from S3
sudo docker load --input ad-rec-flask.tar

# Remove docker image file that was loaded
rm ad-rec-flask.tar

# Run docker image
sudo docker run --rm -d -p 80:80 ad-rec-flask:latest
