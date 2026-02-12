"""
Google Cloud Platform Deployment Configuration
Demonstrates cloud fundamentals and scalable data processing
"""

import json

# GCP Project Configuration
GCP_CONFIG = {
    "project_id": "student-analytics-project",
    "region": "us-central1",
    "zone": "us-central1-a"
}

# Cloud SQL Configuration
CLOUD_SQL_CONFIG = {
    "instance_name": "student-performance-db",
    "database_version": "POSTGRES_14",
    "tier": "db-f1-micro",  # Small instance for development
    "storage_size_gb": 10,
    "backup_enabled": True,
    "backup_start_time": "03:00",
    "database_name": "student_analytics",
    "database_flags": [
        {
            "name": "max_connections",
            "value": "100"
        }
    ]
}

# Cloud Storage Configuration
CLOUD_STORAGE_CONFIG = {
    "bucket_name": "student-analytics-data",
    "storage_class": "STANDARD",
    "location": "US",
    "folders": [
        "raw-data/",
        "processed-data/",
        "analytics-reports/",
        "backups/"
    ]
}

# Cloud Functions Configuration (for serverless analytics)
CLOUD_FUNCTIONS_CONFIG = {
    "function_name": "process-student-data",
    "runtime": "python39",
    "entry_point": "process_data",
    "memory": "256MB",
    "timeout": "60s",
    "trigger_type": "http",
    "environment_variables": {
        "DB_NAME": "student_analytics",
        "BUCKET_NAME": "student-analytics-data"
    }
}

# BigQuery Configuration (for large-scale analytics)
BIGQUERY_CONFIG = {
    "dataset_id": "student_performance_analytics",
    "location": "US",
    "tables": {
        "students": {
            "schema": [
                {"name": "student_id", "type": "INTEGER", "mode": "REQUIRED"},
                {"name": "first_name", "type": "STRING", "mode": "REQUIRED"},
                {"name": "last_name", "type": "STRING", "mode": "REQUIRED"},
                {"name": "email", "type": "STRING", "mode": "REQUIRED"},
                {"name": "enrollment_date", "type": "DATE", "mode": "REQUIRED"},
                {"name": "grade_level", "type": "INTEGER", "mode": "REQUIRED"},
                {"name": "department", "type": "STRING", "mode": "REQUIRED"}
            ]
        },
        "courses": {
            "schema": [
                {"name": "course_id", "type": "INTEGER", "mode": "REQUIRED"},
                {"name": "course_code", "type": "STRING", "mode": "REQUIRED"},
                {"name": "course_name", "type": "STRING", "mode": "REQUIRED"},
                {"name": "department", "type": "STRING", "mode": "REQUIRED"},
                {"name": "credits", "type": "INTEGER", "mode": "REQUIRED"},
                {"name": "difficulty_level", "type": "STRING", "mode": "REQUIRED"}
            ]
        },
        "grades": {
            "schema": [
                {"name": "grade_id", "type": "INTEGER", "mode": "REQUIRED"},
                {"name": "student_id", "type": "INTEGER", "mode": "REQUIRED"},
                {"name": "assessment_id", "type": "INTEGER", "mode": "REQUIRED"},
                {"name": "score", "type": "FLOAT", "mode": "REQUIRED"},
                {"name": "submission_date", "type": "DATE", "mode": "REQUIRED"},
                {"name": "feedback", "type": "STRING", "mode": "NULLABLE"}
            ]
        }
    }
}

# App Engine Configuration (for web application)
APP_ENGINE_CONFIG = {
    "service": "default",
    "runtime": "python39",
    "instance_class": "F1",
    "automatic_scaling": {
        "target_cpu_utilization": 0.65,
        "min_instances": 1,
        "max_instances": 3
    },
    "environment_variables": {
        "CLOUD_SQL_CONNECTION_NAME": f"{GCP_CONFIG['project_id']}:{GCP_CONFIG['region']}:{CLOUD_SQL_CONFIG['instance_name']}"
    }
}

# Cloud Scheduler Configuration (for automated reports)
CLOUD_SCHEDULER_CONFIG = {
    "job_name": "daily-analytics-report",
    "schedule": "0 8 * * *",  # Daily at 8 AM
    "time_zone": "America/New_York",
    "description": "Generate daily student performance analytics report"
}

# Monitoring and Logging Configuration
MONITORING_CONFIG = {
    "alert_policies": [
        {
            "name": "high-database-cpu",
            "condition": "resource.type = cloudsql_database AND metric.type = cloudsql.googleapis.com/database/cpu/utilization > 0.8",
            "notification_channels": ["email"]
        },
        {
            "name": "low-student-performance",
            "condition": "custom.metric.type = student_performance_avg < 70",
            "notification_channels": ["email"]
        }
    ],
    "dashboards": [
        {
            "name": "Student Performance Dashboard",
            "widgets": [
                "Average GPA Trend",
                "Course Enrollment",
                "At-Risk Students",
                "Department Performance"
            ]
        }
    ]
}


def generate_terraform_config():
    """Generate Terraform configuration for GCP infrastructure"""
    terraform_config = f'''
# Terraform Configuration for Student Performance Analytics System

terraform {{
  required_providers {{
    google = {{
      source  = "hashicorp/google"
      version = "~> 4.0"
    }}
  }}
}}

provider "google" {{
  project = "{GCP_CONFIG['project_id']}"
  region  = "{GCP_CONFIG['region']}"
}}

# Cloud SQL Instance
resource "google_sql_database_instance" "student_db" {{
  name             = "{CLOUD_SQL_CONFIG['instance_name']}"
  database_version = "{CLOUD_SQL_CONFIG['database_version']}"
  region           = "{GCP_CONFIG['region']}"

  settings {{
    tier = "{CLOUD_SQL_CONFIG['tier']}"
    
    backup_configuration {{
      enabled    = {str(CLOUD_SQL_CONFIG['backup_enabled']).lower()}
      start_time = "{CLOUD_SQL_CONFIG['backup_start_time']}"
    }}

    ip_configuration {{
      ipv4_enabled = true
      authorized_networks {{
        name  = "all"
        value = "0.0.0.0/0"
      }}
    }}
  }}
}}

resource "google_sql_database" "analytics_db" {{
  name     = "{CLOUD_SQL_CONFIG['database_name']}"
  instance = google_sql_database_instance.student_db.name
}}

# Cloud Storage Bucket
resource "google_storage_bucket" "analytics_data" {{
  name          = "{CLOUD_STORAGE_CONFIG['bucket_name']}"
  location      = "{CLOUD_STORAGE_CONFIG['location']}"
  storage_class = "{CLOUD_STORAGE_CONFIG['storage_class']}"
  
  uniform_bucket_level_access = true
  
  versioning {{
    enabled = true
  }}
}}

# BigQuery Dataset
resource "google_bigquery_dataset" "student_analytics" {{
  dataset_id = "{BIGQUERY_CONFIG['dataset_id']}"
  location   = "{BIGQUERY_CONFIG['location']}"
  
  description = "Student performance analytics dataset"
}}

# Cloud Function
resource "google_cloudfunctions_function" "process_data" {{
  name        = "{CLOUD_FUNCTIONS_CONFIG['function_name']}"
  runtime     = "{CLOUD_FUNCTIONS_CONFIG['runtime']}"
  entry_point = "{CLOUD_FUNCTIONS_CONFIG['entry_point']}"
  
  available_memory_mb = 256
  timeout             = 60
  
  source_archive_bucket = google_storage_bucket.analytics_data.name
  source_archive_object = "function-source.zip"
  
  trigger_http = true
  
  environment_variables = {{
    DB_NAME     = "{CLOUD_SQL_CONFIG['database_name']}"
    BUCKET_NAME = "{CLOUD_STORAGE_CONFIG['bucket_name']}"
  }}
}}

# Cloud Scheduler Job
resource "google_cloud_scheduler_job" "daily_report" {{
  name        = "{CLOUD_SCHEDULER_CONFIG['job_name']}"
  description = "{CLOUD_SCHEDULER_CONFIG['description']}"
  schedule    = "{CLOUD_SCHEDULER_CONFIG['schedule']}"
  time_zone   = "{CLOUD_SCHEDULER_CONFIG['time_zone']}"
  
  http_target {{
    uri         = google_cloudfunctions_function.process_data.https_trigger_url
    http_method = "POST"
  }}
}}
'''
    return terraform_config


def generate_app_yaml():
    """Generate App Engine app.yaml configuration"""
    app_yaml = f'''
runtime: {APP_ENGINE_CONFIG['runtime']}
instance_class: {APP_ENGINE_CONFIG['instance_class']}

automatic_scaling:
  target_cpu_utilization: {APP_ENGINE_CONFIG['automatic_scaling']['target_cpu_utilization']}
  min_instances: {APP_ENGINE_CONFIG['automatic_scaling']['min_instances']}
  max_instances: {APP_ENGINE_CONFIG['automatic_scaling']['max_instances']}

env_variables:
  CLOUD_SQL_CONNECTION_NAME: "{APP_ENGINE_CONFIG['environment_variables']['CLOUD_SQL_CONNECTION_NAME']}"

handlers:
- url: /static
  static_dir: static
  
- url: /.*
  script: auto
'''
    return app_yaml


def generate_requirements_txt():
    """Generate requirements.txt for cloud deployment"""
    requirements = '''
# Core Dependencies
pandas==2.0.3
numpy==1.24.3
SQLAlchemy==2.0.19

# Google Cloud Platform
google-cloud-storage==2.10.0
google-cloud-bigquery==3.11.4
google-cloud-sql-connector==1.3.1
pg8000==1.29.8

# Database Drivers
psycopg2-binary==2.9.6

# Web Framework (if needed)
Flask==2.3.2
gunicorn==21.2.0

# Data Visualization
matplotlib==3.7.2
seaborn==0.12.2

# Utilities
python-dotenv==1.0.0
'''
    return requirements


def save_cloud_configs():
    """Save all cloud configuration files"""
    
    # Save Terraform configuration
    with open('main.tf', 'w') as f:
        f.write(generate_terraform_config())
    
    # Save App Engine configuration
    with open('app.yaml', 'w') as f:
        f.write(generate_app_yaml())
    
    # Save requirements.txt
    with open('requirements.txt', 'w') as f:
        f.write(generate_requirements_txt())
    
    # Save full configuration as JSON
    full_config = {
        "gcp": GCP_CONFIG,
        "cloud_sql": CLOUD_SQL_CONFIG,
        "cloud_storage": CLOUD_STORAGE_CONFIG,
        "cloud_functions": CLOUD_FUNCTIONS_CONFIG,
        "bigquery": BIGQUERY_CONFIG,
        "app_engine": APP_ENGINE_CONFIG,
        "cloud_scheduler": CLOUD_SCHEDULER_CONFIG,
        "monitoring": MONITORING_CONFIG
    }
    
    with open('gcp_config.json', 'w') as f:
        json.dump(full_config, f, indent=2)
    
    print("✓ Cloud configuration files generated successfully!")
    print("  - main.tf (Terraform)")
    print("  - app.yaml (App Engine)")
    print("  - requirements.txt")
    print("  - gcp_config.json")


if __name__ == "__main__":
    save_cloud_configs()
    
    print("\n" + "="*70)
    print("GCP DEPLOYMENT GUIDE")
    print("="*70)
    print("\n1. Initialize Terraform:")
    print("   terraform init")
    print("\n2. Plan infrastructure:")
    print("   terraform plan")
    print("\n3. Deploy infrastructure:")
    print("   terraform apply")
    print("\n4. Deploy application to App Engine:")
    print("   gcloud app deploy app.yaml")
    print("\n5. Deploy Cloud Function:")
    print("   gcloud functions deploy process-student-data --runtime python39")
    print("="*70)
