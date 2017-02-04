#!/bin/bash
# you need httpie and jq (apt-get install httpie jq)

if [ -z ${access_token} ] || [ -z ${name} ] || [ -z ${id} ];then
  echo 'The following environment variables must be set: access_token, name, id'
  exit 1
fi

output_file=world.tar.gz
realms_server=https://mcoapi.minecraft.net
version=1.11.2

cookie_string="Cookie:sid=token:${access_token}:${id};user=${name};version=${version}"

# 1. get world ID
response=$(http --check-status --ignore-stdin GET ${realms_server}/worlds "${cookie_string}")
if [ $? -ne 0 ];then
  echo "Error getting worlds, response: ${response}"
  exit 1
fi
world_id=$(echo ${response} | jq .servers[0].id)

# 2. get download link
response=$(http --check-status --ignore-stdin GET ${realms_server}/worlds/${world_id}/slot/1/download "${cookie_string}")
if [ $? -ne 0 ];then
  echo "Error getting download link, response: ${response}"
  exit 2
fi
url=$(echo ${response} | jq .downloadLink | sed 's/"//g')

# 3. download backup
http --check-status --ignore-stdin --body --download --output ${output_file} ${url}
if [ $? -ne 0 ];then
  echo "Error downloading, exit code: $?"
  exit 3
fi