#!/bin/bash
#Amazon Linux
# Update the package list
sudo yum update -y

# Install git, python3, and pip3
sudo amazon-linux-extras install epel -y
sudo yum install -y git python3 python3-pip

# Upgrade pip
sudo pip3 install --upgrade pip

# Add cloudflared-ascii.repo to /etc/yum.repos.d/ 
curl -fsSl https://pkg.cloudflare.com/cloudflared-ascii.repo | sudo tee /etc/yum.repos.d/cloudflared-ascii.repo

#update repo
sudo yum update -y

# install cloudflared
sudo yum install cloudflared -y