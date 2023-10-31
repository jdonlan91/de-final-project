provider "aws" {
  region = "eu-west-2"
}

terraform {
  backend "s3" {
    bucket = "tfstate-bucket-team-basalt"
    key    = "terraform.tfstate"
    region = "eu-west-2"
  }
}
