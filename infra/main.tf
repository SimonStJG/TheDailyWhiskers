terraform {
  required_version = "0.11.7"

  backend "s3" {
    bucket = "dailywhiskers-tfstate"
    key    = "dailywhiskers.tfstate"
    region = "eu-west-1"
  }
}

provider "aws" {
  region  = "eu-west-1"
  version = "1.24"
}
