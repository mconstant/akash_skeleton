#!/bin/bash

# safe bash boilerplate
set -euo pipefail

source akash_settings.sh

# terraform or tofu
terraform_or_tofu="terraform"

TERRAFORM_VERSION=1.9.2

check_mark=$(printf '\342\234\224' | iconv -f UTF-8 2> /dev/null) ||
  check_mark='[X]'


echo "-------------- Getting Akash Provider Services Version --------------"
provider-services version
# echo unicode checkmark encoded to show in docker compose logs in terminal
echo $check_mark

echo "-------------- Importing Akash Wallet --------------"
echo "$AKASH_SEED_PHRASE
$AKASH_KEYRING_PASSPHRASE
$AKASH_KEYRING_PASSPHRASE" | provider-services keys add $AKASH_KEY_NAME --recover
echo $check_mark

echo "-------------- Determining Akash Account Address --------------"
export AKASH_ACCOUNT_ADDRESS="$(provider-services keys show $AKASH_KEY_NAME -a <<< $AKASH_KEYRING_PASSPHRASE)"
echo $AKASH_ACCOUNT_ADDRESS
export TFE_VAR_akash_account_address=$AKASH_ACCOUNT_ADDRESS
echo $check_mark

echo "-------------- Getting Wallet Account Balance --------------"
provider-services query bank balances --node $AKASH_NODE $AKASH_ACCOUNT_ADDRESS
echo $check_mark

echo "-------------- Create Akash Certificate --------------"
provider-services tx cert generate client --from $AKASH_KEY_NAME <<< $AKASH_KEYRING_PASSPHRASE
echo $check_mark

sleep 3

echo "-------------- Publishing Akash Certificate To Chain --------------"
provider-services tx cert publish client --from $AKASH_KEY_NAME <<< "y\n"
echo $check_mark

echo "-------------- Set Terraform Working Directory --------------"
# set working directory to /terraform
cd /terraform
echo $check_mark

echo "-------------- Set Terraform Vars --------------"
export TFE_VAR_akash_key_name=$AKASH_KEY_NAME
export TFE_VAR_akash_node=$AKASH_NODE
export TFE_VAR_akash_chain_id=$AKASH_CHAIN_ID
echo $check_mark

# echo "-------------- Terraform Cloud Login --------------"
# terraform login
# echo $check_mark

echo "-------------- Create auto.tfvars --------------"
echo "akash_account_address = \"$AKASH_ACCOUNT_ADDRESS\"" > dev.auto.tfvars
echo "akash_key_name = \"$AKASH_KEY_NAME\"" >> dev.auto.tfvars
echo "akash_node = \"$AKASH_NODE\"" >> dev.auto.tfvars
echo "akash_chain_id = \"$AKASH_CHAIN_ID\"" >> dev.auto.tfvars
cat dev.auto.tfvars
echo

echo "-------------- Terraform Init --------------"
$terraform_or_tofu init -backend-config="organization=${TF_ORG_NAME}"
echo $check_mark

echo "-------------- Terraform Plan --------------"
$terraform_or_tofu plan 
echo $check_mark

echo "-------------- Terraform Apply --------------"
$terraform_or_tofu apply -auto-approve 
echo $check_mark