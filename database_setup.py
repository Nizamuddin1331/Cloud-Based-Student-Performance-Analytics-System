"""
Cloud-Based Student Performance Analytics System
Database Setup and Schema Creation
"""

import sqlite3
import random
from datetime import datetime, timedelta
import pandas as pd

class DatabaseSetup:
    def __init__(self, db_name='student_performance.db'):
        """Initialize database connection"""
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        
    def connect(self):
        """Establish database connection"""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        print(f"✓ Connected to database: {self.db_name}")
        
    def create_tables(self):
        """Create database schema for student performance tracking"""
        
        # Students table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                enrollment_date DATE NOT NULL,
                grade_level INTEGER NOT NULL,
                department TEXT NOT NULL
            )
        ''')
        
        # Courses table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS courses (
                course_id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_code TEXT UNIQUE NOT NULL,
                course_name TEXT NOT NULL,
                department TEXT NOT NULL,
                credits INTEGER NOT NULL,
                difficulty_level TEXT CHECK(difficulty_level IN ('Beginner', 'Intermediate', 'Advanced'))
            )
        ''')
        
        # Enrollments table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS enrollments (
                enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                course_id INTEGER NOT NULL,
                enrollment_date DATE NOT NULL,
                semester TEXT NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students(student_id),
                FOREIGN KEY (course_id) REFERENCES courses(course_id)
            )
        ''')
        
        # Assessments table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS assessments (
                assessment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_id INTEGER NOT NULL,
                assessment_type TEXT CHECK(assessment_type IN ('Quiz', 'Midterm', 'Final', 'Project', 'Assignment')),
                assessment_name TEXT NOT NULL,
                max_score REAL NOT NULL,
                weight REAL NOT NULL,
                assessment_date DATE NOT NULL,
                FOREIGN KEY (course_id) REFERENCES courses(course_id)
            )
        ''')
        
        # Grades table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS grades (
                grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                assessment_id INTEGER NOT NULL,
                score REAL NOT NULL,
                submission_date DATE NOT NULL,
                feedback TEXT,
                FOREIGN KEY (student_id) REFERENCES students(student_id),
                FOREIGN KEY (assessment_id) REFERENCES assessments(assessment_id)
            )
        ''')
        
        # Attendance table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                course_id INTEGER NOT NULL,
                attendance_date DATE NOT NULL,
                status TEXT CHECK(status IN ('Present', 'Absent', 'Late', 'Excused')),
                FOREIGN KEY (student_id) REFERENCES students(student_id),
                FOREIGN KEY (course_id) REFERENCES courses(course_id)
            )
        ''')
        
        self.conn.commit()
        print("✓ Database schema created successfully")
        
    def populate_sample_data(self):
        """Populate database with realistic sample data"""
        
        # Sample data
        departments = ['Computer Science', 'Mathematics', 'Physics', 'Engineering', 'Business']
        first_names = ['John', 'Emma', 'Michael', 'Sophia', 'William', 'Olivia', 'James', 'Ava', 
                      'Robert', 'Isabella', 'David', 'Mia', 'Joseph', 'Charlotte', 'Daniel', 'Amelia']
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
                     'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson']
        
        # Insert students
        students_data = []
        for i in range(50):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            email = f"{first_name.lower()}.{last_name.lower()}{i}@university.edu"
            enrollment_date = (datetime.now() - timedelta(days=random.randint(365, 1460))).strftime('%Y-%m-%d')
            grade_level = random.randint(1, 4)
            department = random.choice(departments)
            students_data.append((first_name, last_name, email, enrollment_date, grade_level, department))
        
        self.cursor.executemany('''
            INSERT INTO students (first_name, last_name, email, enrollment_date, grade_level, department)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', students_data)
        
        # Insert courses
        courses_data = [
            ('CS101', 'Introduction to Programming', 'Computer Science', 3, 'Beginner'),
            ('CS201', 'Data Structures', 'Computer Science', 4, 'Intermediate'),
            ('CS301', 'Algorithms', 'Computer Science', 4, 'Advanced'),
            ('MATH101', 'Calculus I', 'Mathematics', 4, 'Beginner'),
            ('MATH201', 'Linear Algebra', 'Mathematics', 3, 'Intermediate'),
            ('PHYS101', 'Physics I', 'Physics', 4, 'Beginner'),
            ('ENG101', 'Engineering Fundamentals', 'Engineering', 3, 'Beginner'),
            ('BUS101', 'Business Analytics', 'Business', 3, 'Intermediate'),
            ('CS202', 'Database Systems', 'Computer Science', 3, 'Intermediate'),
            ('CS302', 'Machine Learning', 'Computer Science', 4, 'Advanced')
        ]
        
        self.cursor.executemany('''
            INSERT INTO courses (course_code, course_name, department, credits, difficulty_level)
            VALUES (?, ?, ?, ?, ?)
        ''', courses_data)
        
        # Insert enrollments
        enrollments_data = []
        semesters = ['Fall 2023', 'Spring 2024', 'Fall 2024']
        for student_id in range(1, 51):
            num_courses = random.randint(3, 5)
            enrolled_courses = random.sample(range(1, 11), num_courses)
            for course_id in enrolled_courses:
                enrollment_date = (datetime.now() - timedelta(days=random.randint(30, 180))).strftime('%Y-%m-%d')
                semester = random.choice(semesters)
                enrollments_data.append((student_id, course_id, enrollment_date, semester))
        
        self.cursor.executemany('''
            INSERT INTO enrollments (student_id, course_id, enrollment_date, semester)
            VALUES (?, ?, ?, ?)
        ''', enrollments_data)
        
        # Insert assessments
        assessment_types = ['Quiz', 'Midterm', 'Final', 'Project', 'Assignment']
        assessments_data = []
        for course_id in range(1, 11):
            for i, assess_type in enumerate(assessment_types):
                assessment_date = (datetime.now() - timedelta(days=random.randint(1, 90))).strftime('%Y-%m-%d')
                max_score = 100.0
                weight = 0.1 if assess_type == 'Quiz' else (0.25 if assess_type in ['Midterm', 'Final'] else 0.15)
                assessments_data.append((course_id, assess_type, f"{assess_type} {i+1}", max_score, weight, assessment_date))
        
        self.cursor.executemany('''
            INSERT INTO assessments (course_id, assessment_type, assessment_name, max_score, weight, assessment_date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', assessments_data)
        
        # Insert grades
        grades_data = []
        for enrollment_id in range(1, len(enrollments_data) + 1):
            # Get student_id and course_id from enrollments
            self.cursor.execute('SELECT student_id, course_id FROM enrollments WHERE enrollment_id = ?', (enrollment_id,))
            student_id, course_id = self.cursor.fetchone()
            
            # Get assessments for this course
            self.cursor.execute('SELECT assessment_id FROM assessments WHERE course_id = ?', (course_id,))
            assessment_ids = [row[0] for row in self.cursor.fetchall()]
            
            for assessment_id in assessment_ids:
                # Generate realistic scores (normal distribution)
                score = max(0, min(100, random.gauss(75, 15)))
                submission_date = (datetime.now() - timedelta(days=random.randint(1, 60))).strftime('%Y-%m-%d')
                feedback = random.choice(['Good work!', 'Needs improvement', 'Excellent!', 'Well done', None])
                grades_data.append((student_id, assessment_id, round(score, 2), submission_date, feedback))
        
        self.cursor.executemany('''
            INSERT INTO grades (student_id, assessment_id, score, submission_date, feedback)
            VALUES (?, ?, ?, ?, ?)
        ''', grades_data)
        
        # Insert attendance records
        attendance_data = []
        statuses = ['Present', 'Absent', 'Late', 'Excused']
        weights = [0.85, 0.05, 0.05, 0.05]  # Most students are present
        
        for enrollment_id in range(1, min(100, len(enrollments_data) + 1)):
            self.cursor.execute('SELECT student_id, course_id FROM enrollments WHERE enrollment_id = ?', (enrollment_id,))
            result = self.cursor.fetchone()
            if result:
                student_id, course_id = result
                for day in range(30):
                    attendance_date = (datetime.now() - timedelta(days=day)).strftime('%Y-%m-%d')
                    status = random.choices(statuses, weights=weights)[0]
                    attendance_data.append((student_id, course_id, attendance_date, status))
        
        self.cursor.executemany('''
            INSERT INTO attendance (student_id, course_id, attendance_date, status)
            VALUES (?, ?, ?, ?)
        ''', attendance_data)
        
        self.conn.commit()
        print("✓ Sample data populated successfully")
        print(f"  - Students: 50")
        print(f"  - Courses: 10")
        print(f"  - Enrollments: {len(enrollments_data)}")
        print(f"  - Assessments: {len(assessments_data)}")
        print(f"  - Grades: {len(grades_data)}")
        print(f"  - Attendance records: {len(attendance_data)}")
        
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("✓ Database connection closed")

if __name__ == "__main__":
    # Initialize and setup database
    db = DatabaseSetup()
    db.connect()
    db.create_tables()
    db.populate_sample_data()
    db.close()
    
    print("\n" + "="*50)
    print("Database setup completed successfully!")
    print("="*50)
