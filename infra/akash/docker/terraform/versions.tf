terraform {
  required_providers {
    akash = {
      source = "akash-network/akash"
      version = "0.1.0"
    }
  }
}

provider "akash" {
  account_address = var.akash_account_address
  home = "/root/.akash"
  key_name = var.akash_key_name
  keyring_backend = "test"
  node = var.akash_node
  chain_id = var.akash_chain_id
  chain_version = local.akash_chain_version
}