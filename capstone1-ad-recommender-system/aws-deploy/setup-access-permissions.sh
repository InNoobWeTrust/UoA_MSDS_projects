#!/usr/bin/env bash

# Load dotenv file (ref: https://gist.github.com/mihow/9c7f559807069a03e302605691f85572?permalink_comment_id=3954807#gistcomment-3954807)
set -o allexport
source .env
set +o allexport

# Substitute S3_BUCKET to the templates
sed 's,{{S3_BUCKET}},'"${S3_BUCKET}"',g' > ./ec2-s3-policy.gen.json < ./ec2-s3-policy.template.json

# Reference for the setup steps: https://icicimov.github.io/blog/docker/Docker-Private-Registry-with-S3-backend-on-AWS/

# Enable trace before calling commands
set -x
# Create policy to access S3
aws iam create-policy --policy-name EC2S3Policy --policy-document file://ec2-s3-policy.gen.json
# Create role with trust policy
aws iam create-role --role-name EC2S3Role --assume-role-policy-document file://ec2-trust-policy.json
# Attach policy to role
aws iam attach-role-policy --role-name EC2S3Role --policy-arn arn:aws:iam::${AWS_ACCOUNT_ID}:policy/EC2S3Policy
# Create instance profile and attach the newly created role
aws iam create-instance-profile --instance-profile-name EC2S3Profile
#aws iam add-role-to-instance-profile --role-name EC2S3Role --instance-profile-name EC2S3Profile
aws iam add-role-to-instance-profile --role-name LabRole --instance-profile-name EC2S3Profile
# Remove created json files after use
rm *.gen.json
