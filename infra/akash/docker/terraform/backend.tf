terraform {
  required_version = "1.9.2"
  backend "remote" {
    hostname = "app.terraform.io"

    workspaces {
        name = "p2s"
    }
  }
}
