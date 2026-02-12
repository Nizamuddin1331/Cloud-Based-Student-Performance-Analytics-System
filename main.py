"""
Main Application Runner
Cloud-Based Student Performance Analytics System
"""

import sys
import os
from datetime import datetime

def print_header():
    """Print application header"""
    print("\n" + "="*80)
    print(" " * 15 + "CLOUD-BASED STUDENT PERFORMANCE ANALYTICS SYSTEM")
    print("="*80)
    print(f"Version: 1.0.0")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80 + "\n")

def print_menu():
    """Display main menu"""
    print("\n📊 MAIN MENU")
    print("-" * 80)
    print("1. Setup Database (Initialize schema and populate sample data)")
    print("2. Run Analytics Reports")
    print("3. Execute SQL Queries")
    print("4. Generate Cloud Deployment Configurations")
    print("5. View System Information")
    print("6. Export Data to CSV")
    print("7. Exit")
    print("-" * 80)

def setup_database():
    """Initialize database with schema and sample data"""
    print("\n🔧 Setting up database...")
    from database_setup import DatabaseSetup
    
    db = DatabaseSetup()
    db.connect()
    db.create_tables()
    db.populate_sample_data()
    db.close()
    
    print("\n✓ Database setup completed successfully!")

def run_analytics():
    """Run comprehensive analytics reports"""
    print("\n📈 Running analytics reports...")
    import subprocess
    result = subprocess.run([sys.executable, 'analytics_engine.py'], 
                          capture_output=False, text=True)
    
    if result.returncode == 0:
        print("\n✓ Analytics reports generated successfully!")

def execute_queries():
    """Execute SQL query examples"""
    print("\n💾 Executing SQL queries...")
    import subprocess
    result = subprocess.run([sys.executable, 'sql_queries.py'], 
                          capture_output=False, text=True)
    
    if result.returncode == 0:
        print("\n✓ SQL queries executed successfully!")

def generate_cloud_config():
    """Generate cloud deployment configurations"""
    print("\n☁️  Generating cloud deployment configurations...")
    import subprocess
    result = subprocess.run([sys.executable, 'cloud_config.py'], 
                          capture_output=False, text=True)
    
    if result.returncode == 0:
        print("\n✓ Cloud configurations generated successfully!")

def export_data():
    """Export data to CSV files"""
    print("\n📤 Exporting data to CSV...")
    
    import sqlite3
    import pandas as pd
    
    conn = sqlite3.connect('student_performance.db')
    
    # Export tables
    tables = ['students', 'courses', 'enrollments', 'assessments', 'grades', 'attendance']
    export_dir = 'exports'
    
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)
    
    for table in tables:
        try:
            df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
            filepath = f"{export_dir}/{table}.csv"
            df.to_csv(filepath, index=False)
            print(f"✓ Exported {table}: {len(df)} records -> {filepath}")
        except Exception as e:
            print(f"✗ Error exporting {table}: {str(e)}")
    
    conn.close()
    print("\n✓ Data export completed!")

def show_system_info():
    """Display system information"""
    print("\nℹ️  SYSTEM INFORMATION")
    print("-" * 80)
    
    import sqlite3
    import pandas as pd
    
    try:
        conn = sqlite3.connect('student_performance.db')
        cursor = conn.cursor()
        
        # Get table counts
        tables_info = [
            ('Students', 'students'),
            ('Courses', 'courses'),
            ('Enrollments', 'enrollments'),
            ('Assessments', 'assessments'),
            ('Grades', 'grades'),
            ('Attendance Records', 'attendance')
        ]
        
        print("\n📊 Database Statistics:")
        print("-" * 80)
        for name, table in tables_info:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"{name:.<25} {count:>10,} records")
        
        # System features
        print("\n🎯 System Features:")
        print("-" * 80)
        features = [
            "✓ SQL Database (SQLite)",
            "✓ Data Analytics with Pandas",
            "✓ Statistical Analysis",
            "✓ Trend Identification",
            "✓ GPA Calculation",
            "✓ At-Risk Student Detection",
            "✓ Course Difficulty Analysis",
            "✓ Attendance Tracking",
            "✓ Department Performance Comparison",
            "✓ Cloud Deployment Ready (GCP)"
        ]
        for feature in features:
            print(f"  {feature}")
        
        # Technologies used
        print("\n🛠️  Technologies:")
        print("-" * 80)
        technologies = [
            "Python 3.x",
            "SQLite / SQL",
            "Pandas (Data Analysis)",
            "NumPy (Statistical Computing)",
            "Google Cloud Platform (Cloud Infrastructure)",
            "Terraform (Infrastructure as Code)",
            "BigQuery (Large-scale Analytics)",
            "Cloud SQL (Managed Database)",
            "Cloud Storage (Object Storage)"
        ]
        for tech in technologies:
            print(f"  • {tech}")
        
        conn.close()
        
    except Exception as e:
        print(f"Error retrieving system information: {str(e)}")
        print("Note: Database may not be initialized. Run option 1 first.")
    
    print("-" * 80)

def main():
    """Main application loop"""
    os.chdir(r'C:\Users\moham\student_performance_analytics')

    
    print_header()
    
    while True:
        print_menu()
        
        try:
            choice = input("\nEnter your choice (1-7): ").strip()
            
            if choice == '1':
                setup_database()
            elif choice == '2':
                run_analytics()
            elif choice == '3':
                execute_queries()
            elif choice == '4':
                generate_cloud_config()
            elif choice == '5':
                show_system_info()
            elif choice == '6':
                export_data()
            elif choice == '7':
                print("\n👋 Thank you for using Student Performance Analytics System!")
                print("Goodbye!\n")
                break
            else:
                print("\n❌ Invalid choice. Please enter a number between 1 and 7.")
            
            input("\nPress Enter to continue...")
            
        except KeyboardInterrupt:
            print("\n\n👋 Application terminated by user. Goodbye!\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
