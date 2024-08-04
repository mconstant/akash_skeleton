resource "akash_deployment" "paytoslay" {
  sdl = file("${path.module}/akash-sdl.yml")
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
