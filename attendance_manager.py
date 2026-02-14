import csv
import os
from datetime import datetime
import pandas as pd

class AttendanceManager:
    def __init__(self):
        self.attendance_dir = "attendance"
        if not os.path.exists(self.attendance_dir):
            os.makedirs(self.attendance_dir)
    
    def export_to_csv(self):
        """Export attendance records to CSV file"""
        from database_handler import DatabaseHandler
        db = DatabaseHandler()
        
        # Get all attendance records
        records = db.get_all_attendance()
        
        if not records:
            print("No attendance records to export")
            return
        
        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.attendance_dir}/attendance_{timestamp}.csv"
        
        # Write to CSV
        with open(filename, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            # Write header
            csvwriter.writerow(['Student ID', 'Name', 'Department', 'Year', 'Timestamp', 'Status'])
            # Write data
            csvwriter.writerows(records)
        
        print(f"Attendance exported to {filename}")
        return filename
    
    def generate_report(self, date=None):
        """Generate attendance report for specific date"""
        from database_handler import DatabaseHandler
        db = DatabaseHandler()
        
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        records = db.get_attendance_by_date(date)
        
        # Create report
        report = f"Attendance Report for {date}\n"
        report += "="*50 + "\n"
        report += f"Total Students Present: {len(records)}\n"
        report += "-"*50 + "\n"
        
        for record in records:
            report += f"ID: {record[0]}, Name: {record[1]}, Time: {record[4]}\n"
        
        return report
    
    def get_statistics(self):
        """Get attendance statistics"""
        from database_handler import DatabaseHandler
        db = DatabaseHandler()
        
        all_records = db.get_all_attendance()
        
        if not all_records:
            return "No attendance records found"
        
        # Calculate statistics
        total_days = len(set(record[4][:10] for record in all_records))
        unique_students = len(set(record[0] for record in all_records))
        
        stats = f"Attendance Statistics\n"
        stats += "="*40 + "\n"
        stats += f"Total Days: {total_days}\n"
        stats += f"Total Students: {unique_students}\n"
        stats += f"Total Records: {len(all_records)}\n"
        
        return stats

if __name__ == "__main__":
    manager = AttendanceManager()
    manager.export_to_csv()
    print(manager.generate_report())
    print(manager.get_statistics())