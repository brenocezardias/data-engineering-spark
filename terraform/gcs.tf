resource "google_storage_bucket" "spark_py" {
  name     = "${local.project}-spark-py"
  location = local.region
  uniform_bucket_level_access = true
  force_destroy = true
}

resource "google_storage_bucket" "spark_files" {
  name     = "${local.project}-spark-files"
  location = local.region
  uniform_bucket_level_access = true
  force_destroy = true
}

