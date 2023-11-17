#!/usr/bin/env bash

# Load dotenv file (ref: https://gist.github.com/mihow/9c7f559807069a03e302605691f85572?permalink_comment_id=3954807#gistcomment-3954807)
set -o allexport
source .env
set +o allexport

# Get current IP in order to add ingress rules
MY_IP=$(curl -s ifconfig.me)

# Enable trace before calling commands
set -x
# Create security group
aws ec2 create-security-group --group-name Ec2SshHttp --description "Allow SSH from current IP and HTTP from anywhere"
# Authorize ingress rules
aws ec2 authorize-security-group-ingress \
    --group-name Ec2SshHttp \
    --ip-permissions \
    IpProtocol=tcp,FromPort=22,ToPort=22,IpRanges="[{CidrIp=${MY_IP}/24}]" \
    IpProtocol=tcp,FromPort=80,ToPort=80,IpRanges="[{CidrIp=0.0.0.0/0}]" \
    IpProtocol=icmp,FromPort=-1,ToPort=-1,IpRanges="[{CidrIp=${MY_IP}/24}]"
