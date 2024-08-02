terraform {
  backend "remote" {
    hostname = "app.terraform.io"

    workspaces {
        name = "p2s"
    }
  }
}
