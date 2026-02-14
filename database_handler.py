import sqlite3
from datetime import datetime
import os

class DatabaseHandler:
    def __init__(self, db_name="attendance.db"):
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        self.connect()
        self.create_tables()
    
    def connect(self):
        """Establish database connection"""
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
    
    def create_tables(self):
        """Create necessary tables if they don't exist"""
        # Students table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                student_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                department TEXT,
                year TEXT,
                registered_date TEXT
            )
        ''')
        
        # Attendance table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT,
                name TEXT,
                department TEXT,
                year TEXT,
                timestamp TEXT,
                status TEXT DEFAULT 'Present',
                FOREIGN KEY (student_id) REFERENCES students (student_id)
            )
        ''')
        
        self.connection.commit()
    
    def add_student(self, student_id, name, department, year):
        """Add new student to database"""
        try:
            registered_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute('''
                INSERT OR REPLACE INTO students (student_id, name, department, year, registered_date)
                VALUES (?, ?, ?, ?, ?)
            ''', (student_id, name, department, year, registered_date))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
    
    def mark_attendance(self, student_id, name, department, year, timestamp):
        """Mark attendance for a student"""
        try:
            # Check if already marked for today
            today = timestamp[:10]
            self.cursor.execute('''
                SELECT * FROM attendance 
                WHERE student_id = ? AND timestamp LIKE ?
            ''', (student_id, f"{today}%"))
            
            if self.cursor.fetchone() is None:
                self.cursor.execute('''
                    INSERT INTO attendance (student_id, name, department, year, timestamp)
                    VALUES (?, ?, ?, ?, ?)
                ''', (student_id, name, department, year, timestamp))
                self.connection.commit()
                
                # Also ensure student exists in students table
                self.add_student(student_id, name, department, year)
                return True
            return False
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
    
    def get_today_attendance(self):
        """Get today's attendance records"""
        today = datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute('''
            SELECT student_id, name, department, year, timestamp, status 
            FROM attendance 
            WHERE timestamp LIKE ?
            ORDER BY timestamp DESC
        ''', (f"{today}%",))
        return self.cursor.fetchall()
    
    def get_all_attendance(self):
        """Get all attendance records"""
        self.cursor.execute('''
            SELECT student_id, name, department, year, timestamp, status 
            FROM attendance 
            ORDER BY timestamp DESC
        ''')
        return self.cursor.fetchall()
    
    def get_attendance_by_date(self, date):
        """Get attendance records for specific date"""
        self.cursor.execute('''
            SELECT student_id, name, department, year, timestamp, status 
            FROM attendance 
            WHERE timestamp LIKE ?
            ORDER BY timestamp DESC
        ''', (f"{date}%",))
        return self.cursor.fetchall()
    
    def get_student_attendance(self, student_id):
        """Get attendance records for specific student"""
        self.cursor.execute('''
            SELECT student_id, name, department, year, timestamp, status 
            FROM attendance 
            WHERE student_id = ?
            ORDER BY timestamp DESC
        ''', (student_id,))
        return self.cursor.fetchall()
    
    def get_student_info(self, student_id):
        """Get student information"""
        self.cursor.execute('''
            SELECT * FROM students WHERE student_id = ?
        ''', (student_id,))
        return self.cursor.fetchone()
    
    def get_all_students(self):
        """Get all registered students"""
        self.cursor.execute('SELECT * FROM students ORDER BY student_id')
        return self.cursor.fetchall()
    
    def delete_attendance_record(self, record_id):
        """Delete specific attendance record"""
        try:
            self.cursor.execute('DELETE FROM attendance WHERE id = ?', (record_id,))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False

if __name__ == "__main__":
    # Test database operations
    db = DatabaseHandler()
    
    # Add test student
    db.add_student("STU001", "John Doe", "Computer Science", "3rd Year")
    
    # Mark attendance
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db.mark_attendance("STU001", "John Doe", "Computer Science", "3rd Year", current_time)
    
    # Get today's attendance
    today_attendance = db.get_today_attendance()
    print("Today's Attendance:", today_attendance)
    
    db.close()