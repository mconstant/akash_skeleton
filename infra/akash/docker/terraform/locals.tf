locals {
  # Split the chain ID at '-' and select the second part (index 1) as the chain version
  akash_chain_version = split("-", var.akash_chain_id)[1]
}