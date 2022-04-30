terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "3.59.0"
    }
  }
  backend "s3" {
    bucket = var.backend
    key    = var.tf_key
    region = var.region
  }
}

provider "aws" {
  region  = var.region
  profile = var.profile
}
