#!/bin/bash
export AKASH_NET="https://raw.githubusercontent.com/akash-network/net/main/mainnet"

export AKASH_CHAIN_ID="$(curl -s "$AKASH_NET/chain-id.txt")"
export AKASH_GAS=auto
export AKASH_GAS_ADJUSTMENT=1.25
export AKASH_GAS_PRICES=0.025uakt
export AKASH_KEYRING_BACKEND=test
export AKASH_NODE="$(curl -s "$AKASH_NET/rpc-nodes.txt" | shuf -n 1)"
export AKASH_SIGN_MODE=amino-json
export AKASH_VERSION="$(curl -s https://api.github.com/repos/akash-network/provider/releases/latest | jq -r '.tag_name')"