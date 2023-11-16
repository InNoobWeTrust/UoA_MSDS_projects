#!/usr/bin/env bash

# Load dotenv file (ref: https://gist.github.com/mihow/9c7f559807069a03e302605691f85572?permalink_comment_id=3954807#gistcomment-3954807)
set -o allexport
source .env
set +o allexport

# Enable trace before calling commands
set -x
# Remove role from instance profile
aws iam remove-role-from-instance-profile --role-name EC2S3Role --instance-profile-name EC2S3Profile
# Delete instance profile
aws iam delete-instance-profile --instance-profile-name EC2S3Profile
# Detach policy from role
aws iam detach-role-policy --role-name EC2S3Role --policy-arn arn:aws:iam::${AWS_ACCOUNT_ID}:policy/EC2S3Policy
# Delete role
aws iam delete-role --role-name EC2S3Role
# Delete policy to access S3
aws iam delete-policy --policy-arn arn:aws:iam::${AWS_ACCOUNT_ID}:policy/EC2S3Policy
