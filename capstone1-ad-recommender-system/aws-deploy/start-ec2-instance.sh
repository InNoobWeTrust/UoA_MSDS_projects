#!/usr/bin/env bash

# Load dotenv file (ref: https://gist.github.com/mihow/9c7f559807069a03e302605691f85572?permalink_comment_id=3954807#gistcomment-3954807)
set -o allexport
source .env
set +o allexport


# Replace bucket string in config file
sed 's,{{S3_BUCKET}},'"${S3_BUCKET}"',g' > ./ec2_bootstrap.gen.sh < ./ec2_bootstrap.template.sh

# Get current IP in order to add ingress rules
MY_IP=$(curl -s ifconfig.me)

# Run instance
INSTANCES=$(set -x; aws ec2 run-instances \
    --image-id ami-0fc5d935ebf8bc3bc \
    --instance-type t2.micro \
    --key-name ${KEY_NAME} \
    --security-groups launch-wizard-1 \
    --user-data file://ec2_bootstrap.gen.sh \
    --private-dns-name-options "HostnameType=ip-name,EnableResourceNameDnsARecord=true,EnableResourceNameDnsAAAARecord=false" \
    --count "1:1" \
    --output text \
    --query "Instances[*].InstanceId")

echo "Created instances: $INSTANCES"
echo $INSTANCES > instances.txt

# Cleanup generated scripts
rm *.gen.sh
