"""
Student Performance Analytics Engine
Performs statistical analysis and trend identification using Python and Pandas
"""

import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime
import json

class PerformanceAnalytics:
    def __init__(self, db_name='student_performance.db'):
        """Initialize analytics engine"""
        self.db_name = db_name
        self.conn = None
        
    def connect(self):
        """Establish database connection"""
        self.conn = sqlite3.connect(self.db_name)
        
    def get_student_performance_summary(self):
        """Get comprehensive performance summary for all students"""
        query = '''
            SELECT 
                s.student_id,
                s.first_name || ' ' || s.last_name AS student_name,
                s.grade_level,
                s.department,
                c.course_name,
                c.difficulty_level,
                AVG(g.score) AS average_score,
                COUNT(DISTINCT a.assessment_id) AS total_assessments,
                MIN(g.score) AS min_score,
                MAX(g.score) AS max_score
            FROM students s
            JOIN enrollments e ON s.student_id = e.student_id
            JOIN courses c ON e.course_id = c.course_id
            JOIN assessments a ON c.course_id = a.course_id
            LEFT JOIN grades g ON s.student_id = g.student_id AND a.assessment_id = g.assessment_id
            GROUP BY s.student_id, c.course_id
            ORDER BY s.student_id, average_score DESC
        '''
        df = pd.read_sql_query(query, self.conn)
        return df
    
    def calculate_gpa(self):
        """Calculate GPA for each student"""
        query = '''
            SELECT 
                s.student_id,
                s.first_name || ' ' || s.last_name AS student_name,
                c.course_code,
                c.course_name,
                c.credits,
                AVG(g.score) AS course_average
            FROM students s
            JOIN enrollments e ON s.student_id = e.student_id
            JOIN courses c ON e.course_id = c.course_id
            JOIN assessments a ON c.course_id = a.course_id
            JOIN grades g ON s.student_id = g.student_id AND a.assessment_id = g.assessment_id
            GROUP BY s.student_id, c.course_id
        '''
        df = pd.read_sql_query(query, self.conn)
        
        # Convert percentage to GPA scale (4.0)
        def score_to_gpa(score):
            if score >= 93: return 4.0
            elif score >= 90: return 3.7
            elif score >= 87: return 3.3
            elif score >= 83: return 3.0
            elif score >= 80: return 2.7
            elif score >= 77: return 2.3
            elif score >= 73: return 2.0
            elif score >= 70: return 1.7
            elif score >= 67: return 1.3
            elif score >= 60: return 1.0
            else: return 0.0
        
        df['grade_points'] = df['course_average'].apply(score_to_gpa)
        df['weighted_points'] = df['grade_points'] * df['credits']
        
        # Calculate GPA by student
        gpa_df = df.groupby(['student_id', 'student_name']).agg({
            'weighted_points': 'sum',
            'credits': 'sum'
        }).reset_index()
        
        gpa_df['GPA'] = (gpa_df['weighted_points'] / gpa_df['credits']).round(2)
        gpa_df = gpa_df[['student_id', 'student_name', 'GPA', 'credits']].sort_values('GPA', ascending=False)
        
        return gpa_df
    
    def identify_at_risk_students(self, threshold=70):
        """Identify students at risk based on performance threshold"""
        query = '''
            SELECT 
                s.student_id,
                s.first_name || ' ' || s.last_name AS student_name,
                s.email,
                c.course_name,
                AVG(g.score) AS average_score,
                COUNT(DISTINCT CASE WHEN g.score < ? THEN g.grade_id END) AS failing_assessments,
                COUNT(DISTINCT g.grade_id) AS total_assessments
            FROM students s
            JOIN enrollments e ON s.student_id = e.student_id
            JOIN courses c ON e.course_id = c.course_id
            JOIN assessments a ON c.course_id = a.course_id
            LEFT JOIN grades g ON s.student_id = g.student_id AND a.assessment_id = g.assessment_id
            GROUP BY s.student_id, c.course_id
            HAVING average_score < ?
            ORDER BY average_score ASC
        '''
        df = pd.read_sql_query(query, self.conn, params=(threshold, threshold))
        df['risk_level'] = df['average_score'].apply(
            lambda x: 'Critical' if x < 60 else ('High' if x < 65 else 'Moderate')
        )
        return df
    
    def course_difficulty_analysis(self):
        """Analyze course difficulty based on student performance"""
        query = '''
            SELECT 
                c.course_code,
                c.course_name,
                c.difficulty_level,
                c.department,
                c.course_id,
                COUNT(DISTINCT e.student_id) AS enrolled_students,
                AVG(g.score) AS average_score,
                MIN(g.score) AS min_score,
                MAX(g.score) AS max_score
            FROM courses c
            JOIN enrollments e ON c.course_id = e.course_id
            JOIN assessments a ON c.course_id = a.course_id
            LEFT JOIN grades g ON a.assessment_id = g.assessment_id
            GROUP BY c.course_id
            ORDER BY average_score ASC
        '''
        df = pd.read_sql_query(query, self.conn)
        
        # Calculate standard deviation using Pandas
        std_devs = []
        for course_id in df['course_id']:
            score_query = f'''
                SELECT g.score
                FROM grades g
                JOIN assessments a ON g.assessment_id = a.assessment_id
                WHERE a.course_id = {course_id}
            '''
            scores = pd.read_sql_query(score_query, self.conn)
            std_devs.append(scores['score'].std() if len(scores) > 0 else 0)
        
        df['score_std_dev'] = std_devs
        df = df.drop('course_id', axis=1)
        
        # Calculate difficulty score (lower average + higher std dev = more difficult)
        df['difficulty_score'] = (100 - df['average_score']) + (df['score_std_dev'] * 0.5)
        df = df.sort_values('difficulty_score', ascending=False)
        
        return df
    
    def attendance_performance_correlation(self):
        """Analyze correlation between attendance and performance"""
        query = '''
            SELECT 
                s.student_id,
                s.first_name || ' ' || s.last_name AS student_name,
                c.course_name,
                COUNT(CASE WHEN at.status = 'Present' THEN 1 END) * 100.0 / 
                    NULLIF(COUNT(at.attendance_id), 0) AS attendance_rate,
                AVG(g.score) AS average_score
            FROM students s
            JOIN enrollments e ON s.student_id = e.student_id
            JOIN courses c ON e.course_id = c.course_id
            LEFT JOIN attendance at ON s.student_id = at.student_id AND c.course_id = at.course_id
            LEFT JOIN assessments a ON c.course_id = a.course_id
            LEFT JOIN grades g ON s.student_id = g.student_id AND a.assessment_id = g.assessment_id
            GROUP BY s.student_id, c.course_id
            HAVING COUNT(at.attendance_id) > 0
        '''
        df = pd.read_sql_query(query, self.conn)
        
        # Calculate correlation
        if len(df) > 0:
            correlation = df['attendance_rate'].corr(df['average_score'])
            df['correlation'] = correlation
        
        return df
    
    def department_performance_comparison(self):
        """Compare performance across departments"""
        query = '''
            SELECT 
                s.department,
                COUNT(DISTINCT s.student_id) AS total_students,
                AVG(g.score) AS average_score,
                MIN(g.score) AS min_score,
                MAX(g.score) AS max_score
            FROM students s
            JOIN enrollments e ON s.student_id = e.student_id
            JOIN assessments a ON e.course_id = a.course_id
            LEFT JOIN grades g ON s.student_id = g.student_id AND a.assessment_id = g.assessment_id
            GROUP BY s.department
            ORDER BY average_score DESC
        '''
        df = pd.read_sql_query(query, self.conn)
        
        # Calculate standard deviation using Pandas
        std_devs = []
        for dept in df['department']:
            score_query = f'''
                SELECT g.score
                FROM grades g
                JOIN students s ON g.student_id = s.student_id
                WHERE s.department = "{dept}"
            '''
            scores = pd.read_sql_query(score_query, self.conn)
            std_devs.append(scores['score'].std() if len(scores) > 0 else 0)
        
        df['score_std_dev'] = std_devs
        
        return df
    
    def assessment_type_analysis(self):
        """Analyze performance by assessment type"""
        query = '''
            SELECT 
                a.assessment_type,
                COUNT(DISTINCT g.student_id) AS students_evaluated,
                AVG(g.score) AS average_score,
                MIN(g.score) AS min_score,
                MAX(g.score) AS max_score,
                COUNT(g.grade_id) AS total_submissions
            FROM assessments a
            LEFT JOIN grades g ON a.assessment_id = g.assessment_id
            GROUP BY a.assessment_type
            ORDER BY average_score DESC
        '''
        df = pd.read_sql_query(query, self.conn)
        
        # Calculate standard deviation using Pandas
        std_devs = []
        for assess_type in df['assessment_type']:
            score_query = f'''
                SELECT g.score
                FROM grades g
                JOIN assessments a ON g.assessment_id = a.assessment_id
                WHERE a.assessment_type = "{assess_type}"
            '''
            scores = pd.read_sql_query(score_query, self.conn)
            std_devs.append(scores['score'].std() if len(scores) > 0 else 0)
        
        df['score_std_dev'] = std_devs
        
        return df
    
    def trend_analysis_over_time(self):
        """Identify performance trends over time"""
        query = '''
            SELECT 
                DATE(g.submission_date) AS submission_date,
                AVG(g.score) AS average_score,
                COUNT(g.grade_id) AS submissions,
                COUNT(DISTINCT g.student_id) AS unique_students
            FROM grades g
            GROUP BY DATE(g.submission_date)
            ORDER BY submission_date
        '''
        df = pd.read_sql_query(query, self.conn)
        df['submission_date'] = pd.to_datetime(df['submission_date'])
        
        # Calculate moving average
        if len(df) > 7:
            df['7_day_avg'] = df['average_score'].rolling(window=7, min_periods=1).mean()
        
        return df
    
    def top_performers(self, limit=10):
        """Get top performing students"""
        gpa_df = self.calculate_gpa()
        return gpa_df.head(limit)
    
    def generate_analytics_report(self):
        """Generate comprehensive analytics report"""
        report = {
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'summary': {},
            'insights': []
        }
        
        # Overall statistics
        gpa_df = self.calculate_gpa()
        report['summary']['average_gpa'] = round(gpa_df['GPA'].mean(), 2)
        report['summary']['median_gpa'] = round(gpa_df['GPA'].median(), 2)
        report['summary']['total_students'] = len(gpa_df)
        
        # At-risk students
        at_risk = self.identify_at_risk_students()
        report['summary']['at_risk_students'] = len(at_risk)
        
        # Department comparison
        dept_perf = self.department_performance_comparison()
        best_dept = dept_perf.iloc[0]
        report['insights'].append({
            'type': 'best_department',
            'department': best_dept['department'],
            'average_score': round(best_dept['average_score'], 2)
        })
        
        # Course difficulty
        course_diff = self.course_difficulty_analysis()
        hardest_course = course_diff.iloc[0]
        report['insights'].append({
            'type': 'hardest_course',
            'course': hardest_course['course_name'],
            'average_score': round(hardest_course['average_score'], 2)
        })
        
        # Attendance correlation
        attendance_corr = self.attendance_performance_correlation()
        if len(attendance_corr) > 0 and 'correlation' in attendance_corr.columns:
            corr_value = attendance_corr['correlation'].iloc[0] if len(attendance_corr) > 0 else 0
            report['insights'].append({
                'type': 'attendance_correlation',
                'correlation': round(corr_value, 3),
                'interpretation': 'Strong positive' if corr_value > 0.7 else ('Moderate' if corr_value > 0.4 else 'Weak')
            })
        
        return report
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

if __name__ == "__main__":
    # Run analytics
    analytics = PerformanceAnalytics()
    analytics.connect()
    
    print("="*70)
    print("STUDENT PERFORMANCE ANALYTICS REPORT")
    print("="*70)
    
    # GPA Analysis
    print("\n📊 GPA ANALYSIS - Top 10 Students")
    print("-"*70)
    gpa_df = analytics.calculate_gpa()
    print(gpa_df.head(10).to_string(index=False))
    
    # At-Risk Students
    print("\n⚠️  AT-RISK STUDENTS (Score < 70)")
    print("-"*70)
    at_risk = analytics.identify_at_risk_students()
    if len(at_risk) > 0:
        print(at_risk.head(10).to_string(index=False))
    else:
        print("No at-risk students identified.")
    
    # Course Difficulty
    print("\n📚 COURSE DIFFICULTY ANALYSIS")
    print("-"*70)
    course_diff = analytics.course_difficulty_analysis()
    print(course_diff.to_string(index=False))
    
    # Department Performance
    print("\n🏛️  DEPARTMENT PERFORMANCE COMPARISON")
    print("-"*70)
    dept_perf = analytics.department_performance_comparison()
    print(dept_perf.to_string(index=False))
    
    # Assessment Type Analysis
    print("\n📝 ASSESSMENT TYPE ANALYSIS")
    print("-"*70)
    assess_type = analytics.assessment_type_analysis()
    print(assess_type.to_string(index=False))
    
    # Generate Report
    print("\n📈 COMPREHENSIVE ANALYTICS REPORT")
    print("-"*70)
    report = analytics.generate_analytics_report()
    print(json.dumps(report, indent=2))
    
    analytics.close()
    print("\n" + "="*70)
    print("Analytics completed successfully!")
    print("="*70)
