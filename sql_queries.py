"""
SQL Query Examples for Student Performance Analytics
Demonstrates structured data querying capabilities
"""

# Complex SQL queries for various analytics scenarios

QUERIES = {
    
    # 1. Student Performance Overview
    "student_performance_overview": """
        SELECT 
            s.student_id,
            s.first_name || ' ' || s.last_name AS student_name,
            s.department,
            s.grade_level,
            COUNT(DISTINCT e.course_id) AS courses_enrolled,
            AVG(g.score) AS overall_average,
            MIN(g.score) AS lowest_score,
            MAX(g.score) AS highest_score,
            ROUND(STDEV(g.score), 2) AS score_variability
        FROM students s
        LEFT JOIN enrollments e ON s.student_id = e.student_id
        LEFT JOIN assessments a ON e.course_id = a.course_id
        LEFT JOIN grades g ON s.student_id = g.student_id AND a.assessment_id = g.assessment_id
        GROUP BY s.student_id
        ORDER BY overall_average DESC;
    """,
    
    # 2. Course Performance by Difficulty Level
    "course_difficulty_performance": """
        SELECT 
            c.difficulty_level,
            COUNT(DISTINCT c.course_id) AS total_courses,
            COUNT(DISTINCT e.student_id) AS total_enrollments,
            ROUND(AVG(g.score), 2) AS average_score,
            ROUND(MIN(g.score), 2) AS min_score,
            ROUND(MAX(g.score), 2) AS max_score
        FROM courses c
        JOIN enrollments e ON c.course_id = e.course_id
        JOIN assessments a ON c.course_id = a.course_id
        LEFT JOIN grades g ON a.assessment_id = g.assessment_id AND e.student_id = g.student_id
        GROUP BY c.difficulty_level
        ORDER BY average_score DESC;
    """,
    
    # 3. Identify High-Performing Students per Course
    "top_students_per_course": """
        WITH CourseAverages AS (
            SELECT 
                c.course_code,
                c.course_name,
                s.student_id,
                s.first_name || ' ' || s.last_name AS student_name,
                AVG(g.score) AS course_average,
                RANK() OVER (PARTITION BY c.course_id ORDER BY AVG(g.score) DESC) AS rank
            FROM courses c
            JOIN enrollments e ON c.course_id = e.course_id
            JOIN students s ON e.student_id = s.student_id
            JOIN assessments a ON c.course_id = a.course_id
            LEFT JOIN grades g ON s.student_id = g.student_id AND a.assessment_id = g.assessment_id
            GROUP BY c.course_id, s.student_id
        )
        SELECT course_code, course_name, student_name, ROUND(course_average, 2) AS average
        FROM CourseAverages
        WHERE rank <= 3
        ORDER BY course_code, rank;
    """,
    
    # 4. Assessment Type Performance Analysis
    "assessment_performance": """
        SELECT 
            a.assessment_type,
            c.course_name,
            COUNT(g.grade_id) AS total_submissions,
            ROUND(AVG(g.score), 2) AS average_score,
            ROUND(AVG(a.weight) * 100, 1) AS average_weight_percent
        FROM assessments a
        JOIN courses c ON a.course_id = c.course_id
        LEFT JOIN grades g ON a.assessment_id = g.assessment_id
        GROUP BY a.assessment_type, c.course_name
        ORDER BY a.assessment_type, average_score DESC;
    """,
    
    # 5. Semester Performance Trends
    "semester_trends": """
        SELECT 
            e.semester,
            COUNT(DISTINCT s.student_id) AS total_students,
            COUNT(DISTINCT c.course_id) AS total_courses,
            ROUND(AVG(g.score), 2) AS average_score,
            COUNT(CASE WHEN g.score >= 90 THEN 1 END) AS a_grades,
            COUNT(CASE WHEN g.score >= 80 AND g.score < 90 THEN 1 END) AS b_grades,
            COUNT(CASE WHEN g.score >= 70 AND g.score < 80 THEN 1 END) AS c_grades,
            COUNT(CASE WHEN g.score < 70 THEN 1 END) AS below_c
        FROM enrollments e
        JOIN students s ON e.student_id = s.student_id
        JOIN courses c ON e.course_id = c.course_id
        JOIN assessments a ON c.course_id = a.course_id
        LEFT JOIN grades g ON s.student_id = g.student_id AND a.assessment_id = g.assessment_id
        GROUP BY e.semester
        ORDER BY e.semester DESC;
    """,
    
    # 6. Attendance Impact on Performance
    "attendance_impact": """
        SELECT 
            s.student_id,
            s.first_name || ' ' || s.last_name AS student_name,
            c.course_name,
            COUNT(at.attendance_id) AS total_classes,
            SUM(CASE WHEN at.status = 'Present' THEN 1 ELSE 0 END) AS classes_attended,
            ROUND(SUM(CASE WHEN at.status = 'Present' THEN 1 ELSE 0 END) * 100.0 / 
                  NULLIF(COUNT(at.attendance_id), 0), 1) AS attendance_percentage,
            ROUND(AVG(g.score), 2) AS average_score
        FROM students s
        JOIN enrollments e ON s.student_id = e.student_id
        JOIN courses c ON e.course_id = c.course_id
        LEFT JOIN attendance at ON s.student_id = at.student_id AND c.course_id = at.course_id
        LEFT JOIN assessments a ON c.course_id = a.course_id
        LEFT JOIN grades g ON s.student_id = g.student_id AND a.assessment_id = g.assessment_id
        GROUP BY s.student_id, c.course_id
        HAVING COUNT(at.attendance_id) > 0
        ORDER BY attendance_percentage DESC;
    """,
    
    # 7. Department Comparison
    "department_comparison": """
        SELECT 
            s.department,
            COUNT(DISTINCT s.student_id) AS total_students,
            COUNT(DISTINCT e.course_id) AS total_courses,
            ROUND(AVG(g.score), 2) AS average_score,
            COUNT(CASE WHEN g.score >= 80 THEN 1 END) AS high_performers,
            COUNT(CASE WHEN g.score < 70 THEN 1 END) AS at_risk_count,
            ROUND(AVG(CASE WHEN at.status = 'Present' THEN 1 ELSE 0 END) * 100, 1) AS avg_attendance
        FROM students s
        LEFT JOIN enrollments e ON s.student_id = e.student_id
        LEFT JOIN assessments a ON e.course_id = a.course_id
        LEFT JOIN grades g ON s.student_id = g.student_id AND a.assessment_id = g.assessment_id
        LEFT JOIN attendance at ON s.student_id = at.student_id AND e.course_id = at.course_id
        GROUP BY s.department
        ORDER BY average_score DESC;
    """,
    
    # 8. Recent Performance Trends (Last 30 Days)
    "recent_trends": """
        SELECT 
            DATE(g.submission_date) AS date,
            COUNT(DISTINCT g.student_id) AS students_evaluated,
            COUNT(g.grade_id) AS total_submissions,
            ROUND(AVG(g.score), 2) AS daily_average,
            COUNT(CASE WHEN g.score >= 90 THEN 1 END) AS excellent,
            COUNT(CASE WHEN g.score >= 70 AND g.score < 90 THEN 1 END) AS satisfactory,
            COUNT(CASE WHEN g.score < 70 THEN 1 END) AS needs_improvement
        FROM grades g
        WHERE g.submission_date >= DATE('now', '-30 days')
        GROUP BY DATE(g.submission_date)
        ORDER BY date DESC;
    """,
    
    # 9. Student Progress Tracking
    "student_progress": """
        WITH FirstHalf AS (
            SELECT 
                s.student_id,
                AVG(g.score) AS first_half_avg
            FROM students s
            JOIN grades g ON s.student_id = g.student_id
            WHERE g.submission_date <= DATE('now', '-30 days')
            GROUP BY s.student_id
        ),
        SecondHalf AS (
            SELECT 
                s.student_id,
                AVG(g.score) AS second_half_avg
            FROM students s
            JOIN grades g ON s.student_id = g.student_id
            WHERE g.submission_date > DATE('now', '-30 days')
            GROUP BY s.student_id
        )
        SELECT 
            s.student_id,
            s.first_name || ' ' || s.last_name AS student_name,
            ROUND(fh.first_half_avg, 2) AS early_average,
            ROUND(sh.second_half_avg, 2) AS recent_average,
            ROUND(sh.second_half_avg - fh.first_half_avg, 2) AS improvement,
            CASE 
                WHEN sh.second_half_avg - fh.first_half_avg > 5 THEN 'Improving'
                WHEN sh.second_half_avg - fh.first_half_avg < -5 THEN 'Declining'
                ELSE 'Stable'
            END AS trend
        FROM students s
        LEFT JOIN FirstHalf fh ON s.student_id = fh.student_id
        LEFT JOIN SecondHalf sh ON s.student_id = sh.student_id
        WHERE fh.first_half_avg IS NOT NULL AND sh.second_half_avg IS NOT NULL
        ORDER BY improvement DESC;
    """,
    
    # 10. Course Completion and Success Rates
    "course_completion_rates": """
        SELECT 
            c.course_code,
            c.course_name,
            c.difficulty_level,
            COUNT(DISTINCT e.student_id) AS enrolled_students,
            COUNT(DISTINCT g.student_id) AS students_with_grades,
            ROUND(COUNT(DISTINCT g.student_id) * 100.0 / 
                  COUNT(DISTINCT e.student_id), 1) AS completion_rate,
            ROUND(AVG(g.score), 2) AS average_score,
            COUNT(CASE WHEN g.score >= 70 THEN 1 END) * 100.0 / 
                NULLIF(COUNT(g.grade_id), 0) AS pass_rate
        FROM courses c
        LEFT JOIN enrollments e ON c.course_id = e.course_id
        LEFT JOIN assessments a ON c.course_id = a.course_id
        LEFT JOIN grades g ON e.student_id = g.student_id AND a.assessment_id = g.assessment_id
        GROUP BY c.course_id
        ORDER BY completion_rate DESC;
    """
}


def run_query(db_name, query_name):
    """Execute a specific query and return results"""
    import sqlite3
    import pandas as pd
    
    if query_name not in QUERIES:
        print(f"Query '{query_name}' not found!")
        return None
    
    conn = sqlite3.connect(db_name)
    df = pd.read_sql_query(QUERIES[query_name], conn)
    conn.close()
    
    return df


if __name__ == "__main__":
    import sqlite3
    import pandas as pd
    
    db_name = 'student_performance.db'
    
    print("="*80)
    print("SQL QUERY EXAMPLES - STUDENT PERFORMANCE ANALYTICS")
    print("="*80)
    
    # Run and display each query
    for query_name, query in QUERIES.items():
        print(f"\n{'='*80}")
        print(f"Query: {query_name.upper().replace('_', ' ')}")
        print(f"{'='*80}")
        
        try:
            conn = sqlite3.connect(db_name)
            df = pd.read_sql_query(query, conn)
            conn.close()
            
            if len(df) > 0:
                # Show first 10 rows
                print(df.head(10).to_string(index=False))
                if len(df) > 10:
                    print(f"\n... and {len(df) - 10} more rows")
            else:
                print("No results found.")
        except Exception as e:
            print(f"Error executing query: {str(e)}")
    
    print("\n" + "="*80)
    print("All queries executed successfully!")
    print("="*80)
