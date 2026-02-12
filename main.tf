
# Terraform Configuration for Student Performance Analytics System

terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}

provider "google" {
  project = "student-analytics-project"
  region  = "us-central1"
}

# Cloud SQL Instance
resource "google_sql_database_instance" "student_db" {
  name             = "student-performance-db"
  database_version = "POSTGRES_14"
  region           = "us-central1"

  settings {
    tier = "db-f1-micro"
    
    backup_configuration {
      enabled    = true
      start_time = "03:00"
    }

    ip_configuration {
      ipv4_enabled = true
      authorized_networks {
        name  = "all"
        value = "0.0.0.0/0"
      }
    }
  }
}

resource "google_sql_database" "analytics_db" {
  name     = "student_analytics"
  instance = google_sql_database_instance.student_db.name
}

# Cloud Storage Bucket
resource "google_storage_bucket" "analytics_data" {
  name          = "student-analytics-data"
  location      = "US"
  storage_class = "STANDARD"
  
  uniform_bucket_level_access = true
  
  versioning {
    enabled = true
  }
}

# BigQuery Dataset
resource "google_bigquery_dataset" "student_analytics" {
  dataset_id = "student_performance_analytics"
  location   = "US"
  
  description = "Student performance analytics dataset"
}

# Cloud Function
resource "google_cloudfunctions_function" "process_data" {
  name        = "process-student-data"
  runtime     = "python39"
  entry_point = "process_data"
  
  available_memory_mb = 256
  timeout             = 60
  
  source_archive_bucket = google_storage_bucket.analytics_data.name
  source_archive_object = "function-source.zip"
  
  trigger_http = true
  
  environment_variables = {
    DB_NAME     = "student_analytics"
    BUCKET_NAME = "student-analytics-data"
  }
}

# Cloud Scheduler Job
resource "google_cloud_scheduler_job" "daily_report" {
  name        = "daily-analytics-report"
  description = "Generate daily student performance analytics report"
  schedule    = "0 8 * * *"
  time_zone   = "America/New_York"
  
  http_target {
    uri         = google_cloudfunctions_function.process_data.https_trigger_url
    http_method = "POST"
  }
}
