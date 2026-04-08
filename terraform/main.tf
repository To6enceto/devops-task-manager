terraform {
  required_version = ">= 1.7.0"

  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.40"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.14"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.31"
    }
  }

  # DigitalOcean Spaces (S3-compatible) backend
  # Run: terraform init \
  #   -backend-config="access_key=<SPACES_ACCESS_KEY>" \
  #   -backend-config="secret_key=<SPACES_SECRET_KEY>"
  backend "s3" {
    endpoint                    = "https://ams3.digitaloceanspaces.com"
    bucket                      = "devops-task-manager-tf-state"
    key                         = "terraform/state"
    region                      = "us-east-1" # required field, ignored by Spaces
    skip_credentials_validation = true
    skip_metadata_api_check     = true
    skip_region_validation      = true
    force_path_style            = true
  }
}
