terraform {
  backend "gcs" {
    bucket = "YOUR_PROJECT_ID-terraform-magalu"
    prefix = "terraform/state"
  }
}

provider "google" {
  project = local.project
  region  = local.region
  zone    = local.zone
}
