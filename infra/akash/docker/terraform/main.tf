resource "akash_deployment" "paytoslay" {
  sdl = <<EOF
---
version: "2.0"

services:
  banano-node:
    image: xmconstantx/configurable-bananode:latest
    env:
      - CONFIG_NODE_WEBSOCKET_ENABLE=true
      - CONFIG_NODE_RPC_ENABLE=true
      - CONFIG_RPC_ENABLE_CONTROL=false
      - CONFIG_NODE_ROCKSDB_ENABLE=true
      - CONFIG_SNAPSHOT_URL=https://ledgerfiles.moonano.net/files/latest.tar.gz
    expose:
      - port: 7071
        to:
          - global: false
      - port: 7072
        to:
          - global: true
      - port: 7074
        to:
          - global: false
profiles:
  compute:
    banano-node:
      resources:
        cpu:
          units: 2
        memory:
          size: 512Mi
        storage:
          size: 50Gi
  placement:
    akash:
      attributes:
        host: akash
      signedBy:
        anyOf:
          - "akash1365yvmc4s7awdyj3n2sav7xfx76adc6dnmlx63"
          - "akash18qa2a2ltfyvkyj0ggj3hkvuj6twzyumuaru9s4"
      pricing:
        banano-node: 
          denom: uakt
          amount: 100
deployment:
  banano-node:
    akash:
      profile: banano-node
      count: 1 
EOF
}

data "akash_providers" "us_providers" {
  all_providers = false
  minimum_uptime = 99
  required_attributes = {
    region = "us-east"
  }
}

output "provider_address" {
  value = akash_deployment.paytoslay.provider_address
}

output "services" {
  value = akash_deployment.paytoslay.services
}

output "deployment_dseq" {
  value = akash_deployment.paytoslay.deployment_dseq
}

output "deployment_gseq" {
  value = akash_deployment.paytoslay.deployment_gseq
}

output "deployment_oseq" {
  value = akash_deployment.paytoslay.deployment_oseq
}
