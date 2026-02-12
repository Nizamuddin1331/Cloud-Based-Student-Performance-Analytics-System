# Cloud-Based Student Performance Analytics System

A comprehensive data analytics system designed to evaluate student academic performance using Python, SQL, Google Cloud Platform, and Pandas. This project demonstrates cloud fundamentals, scalable data processing, statistical analysis, and trend identification.

## 🎯 Project Overview

This system provides educational institutions with powerful tools to:
- Track and analyze student academic performance
- Identify at-risk students early
- Compare performance across departments and courses
- Analyze attendance patterns and their impact on grades
- Generate actionable insights through statistical analysis
- Scale to handle large datasets using cloud infrastructure

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Web Interface / API                      │
│                    (Google App Engine)                       │
└────────────────────────┬────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
┌────────▼──────┐ ┌─────▼──────┐ ┌──────▼───────┐
│  Cloud SQL    │ │  BigQuery  │ │Cloud Storage │
│  (PostgreSQL) │ │ (Analytics)│ │ (Data Lake)  │
└───────────────┘ └────────────┘ └──────────────┘
         │               │               │
         └───────────────┼───────────────┘
                         │
              ┌──────────▼──────────┐
              │  Cloud Functions    │
              │  (Data Processing)  │
              └─────────────────────┘
```

## ✨ Features

### Core Functionality
- **Student Performance Tracking**: Comprehensive grade management and GPA calculation
- **Statistical Analysis**: Mean, median, standard deviation, and trend analysis
- **Risk Assessment**: Automatic identification of at-risk students
- **Course Analytics**: Difficulty analysis and success rate tracking
- **Attendance Correlation**: Impact analysis of attendance on performance
- **Department Comparison**: Cross-departmental performance metrics

### Technical Capabilities
- **SQL Database Management**: Structured data storage with relational integrity
- **Data Analytics with Pandas**: Advanced data manipulation and analysis
- **Cloud-Ready Architecture**: Designed for Google Cloud Platform deployment
- **Scalable Design**: Handles growing datasets efficiently
- **Automated Reporting**: Scheduled analytics reports
- **Data Export**: CSV export functionality for external analysis

## 📁 Project Structure

```
student_performance_analytics/
│
├── main.py                  # Main application runner with menu interface
├── database_setup.py        # Database schema creation and sample data
├── analytics_engine.py      # Statistical analysis and trend identification
├── sql_queries.py           # Complex SQL query examples
├── cloud_config.py          # GCP deployment configurations
│
├── main.tf                  # Terraform infrastructure as code
├── app.yaml                 # App Engine configuration
├── requirements.txt         # Python dependencies
├── gcp_config.json         # GCP configuration parameters
│
├── README.md               # This file
└── exports/                # CSV export directory
```

## 🚀 Getting Started

### Prerequisites

```bash
# Python 3.8 or higher
python --version

# Required Python packages
pip install pandas numpy sqlite3
```

### Installation

1. **Clone or download the project files**

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Initialize the database**:
```bash
python main.py
# Select option 1: Setup Database
```

### Quick Start

Run the main application:
```bash
python main.py
```

The application provides an interactive menu with the following options:
1. Setup Database (Initialize schema and populate sample data)
2. Run Analytics Reports
3. Execute SQL Queries
4. Generate Cloud Deployment Configurations
5. View System Information
6. Export Data to CSV
7. Exit

## 📊 Database Schema

### Tables

**students**
- student_id (PRIMARY KEY)
- first_name, last_name
- email (UNIQUE)
- enrollment_date
- grade_level
- department

**courses**
- course_id (PRIMARY KEY)
- course_code (UNIQUE)
- course_name
- department
- credits
- difficulty_level

**enrollments**
- enrollment_id (PRIMARY KEY)
- student_id (FOREIGN KEY)
- course_id (FOREIGN KEY)
- enrollment_date
- semester

**assessments**
- assessment_id (PRIMARY KEY)
- course_id (FOREIGN KEY)
- assessment_type
- assessment_name
- max_score, weight
- assessment_date

**grades**
- grade_id (PRIMARY KEY)
- student_id (FOREIGN KEY)
- assessment_id (FOREIGN KEY)
- score
- submission_date
- feedback

**attendance**
- attendance_id (PRIMARY KEY)
- student_id (FOREIGN KEY)
- course_id (FOREIGN KEY)
- attendance_date
- status

## 🔍 Analytics Features

### 1. GPA Calculation
Converts percentage scores to 4.0 scale GPA with weighted credit hours.

### 2. At-Risk Student Identification
Identifies students with:
- Average scores below threshold (default: 70%)
- Multiple failing assessments
- Risk levels: Critical (<60%), High (<65%), Moderate (<70%)

### 3. Course Difficulty Analysis
Evaluates courses based on:
- Average student performance
- Score variance
- Enrollment statistics

### 4. Attendance Impact Analysis
Correlates attendance rates with academic performance:
- Attendance percentage calculation
- Performance comparison
- Statistical correlation metrics

### 5. Trend Analysis
Tracks performance over time:
- Daily/weekly/monthly trends
- Moving averages
- Improvement/decline detection

### 6. Department Comparison
Compares performance metrics across departments:
- Average scores
- Student counts
- Performance distribution

## 💾 SQL Query Examples

The system includes 10 complex SQL queries demonstrating:
- JOIN operations across multiple tables
- Aggregate functions (AVG, COUNT, MIN, MAX, STDEV)
- Window functions (RANK, PARTITION BY)
- Common Table Expressions (CTEs)
- Subqueries
- Date functions
- Conditional aggregation (CASE statements)

Access these queries through:
```bash
python sql_queries.py
```

## ☁️ Cloud Deployment (Google Cloud Platform)

### Architecture Components

1. **Cloud SQL** - Managed PostgreSQL database
2. **BigQuery** - Large-scale analytics
3. **Cloud Storage** - Data lake for raw/processed data
4. **Cloud Functions** - Serverless data processing
5. **App Engine** - Web application hosting
6. **Cloud Scheduler** - Automated report generation

### Deployment Steps

1. **Generate cloud configurations**:
```bash
python cloud_config.py
```

2. **Initialize Terraform**:
```bash
terraform init
terraform plan
terraform apply
```

3. **Deploy to App Engine**:
```bash
gcloud app deploy app.yaml
```

4. **Deploy Cloud Function**:
```bash
gcloud functions deploy process-student-data --runtime python39
```

### Cost Estimation (Monthly)
- Cloud SQL (db-f1-micro): ~$7
- Cloud Storage (10GB): ~$0.20
- Cloud Functions (100K invocations): ~$0.40
- App Engine (F1 instance): ~$50
- BigQuery (1TB queries): ~$5
- **Total**: ~$62/month

## 📈 Sample Analytics Output

### GPA Analysis
```
student_id  student_name      GPA  credits
1          John Smith        3.85     15
2          Emma Johnson      3.72     12
3          Michael Williams  3.68     15
```

### At-Risk Students
```
student_id  student_name  course_name          avg_score  risk_level
15         David Brown   Algorithms           58.5       Critical
23         Sarah Davis   Machine Learning     63.2       High
```

### Course Difficulty
```
course_code  course_name        avg_score  difficulty_score
CS301       Algorithms          68.5       42.3
CS302       Machine Learning    71.2       38.5
MATH201     Linear Algebra      75.8       32.1
```

## 🛠️ Technologies Used

- **Python 3.x** - Core programming language
- **SQLite/PostgreSQL** - Database management
- **Pandas** - Data analysis and manipulation
- **NumPy** - Statistical computing
- **Google Cloud Platform** - Cloud infrastructure
  - Cloud SQL
  - BigQuery
  - Cloud Storage
  - Cloud Functions
  - App Engine
  - Cloud Scheduler
- **Terraform** - Infrastructure as Code

## 📦 Data Export

Export all data to CSV files:
```bash
python main.py
# Select option 6: Export Data to CSV
```

Exports include:
- students.csv
- courses.csv
- enrollments.csv
- assessments.csv
- grades.csv
- attendance.csv

## 🔒 Security Considerations

- Database credentials stored in environment variables
- SQL injection prevention through parameterized queries
- Cloud IAM roles for access control
- SSL/TLS encryption for data in transit
- Encrypted storage for sensitive data

## 📊 Performance Optimizations

1. **Database Indexing**: Primary keys and foreign keys for fast lookups
2. **Query Optimization**: Efficient JOINs and aggregations
3. **Batch Processing**: Bulk inserts for large datasets
4. **Caching**: Frequently accessed analytics cached
5. **Partitioning**: BigQuery tables partitioned by date

## 🤝 Contributing

This is a demonstration project. For production use:
1. Implement user authentication
2. Add input validation and sanitization
3. Enhance error handling
4. Add comprehensive logging
5. Implement data backup strategies
6. Add monitoring and alerting

## 📄 License

This project is open-source and available for educational, learning, and demonstration purposes.

You are free to use, modify, and distribute this project with proper attribution.

For commercial usage or large-scale deployment, please ensure appropriate modifications and validation are performed.

👨‍💻 Author

Mohammed Nizamuddin
B.Tech in Computer Science and Engineering

## 📧 Contact

If you have any questions, suggestions, or would like to collaborate, feel free to reach out:

Mohammed Nizamuddin
📧 mohammednizamuddin072003@gmail.com

🔗 LinkedIn: https://www.linkedin.com/in/mohammed-nizamuddin-3b79bb26b/

You can also open an issue in this repository for discussions, improvements, or feature requests.

## 🙏 Acknowledgments

- Sample data generated using realistic educational scenarios
- Database design follows academic information system best practices
- Cloud architecture based on GCP reference architectures
- Statistical methods aligned with educational assessment standards

---

**Version**: 1.0.0  
**Last Updated**: 2025  
**Status**: Production Ready (with additional security measures recommended)
