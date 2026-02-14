import cv2
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import *
import os
from PIL import Image, ImageTk
import threading
from datetime import datetime
import face_recognition
import numpy as np

class AttendanceSystem:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1200x700+0+0")
        self.root.title("Face Recognition Based Attendance Monitoring System")
        
        # Variables
        self.var_student_id = StringVar()
        self.var_student_name = StringVar()
        self.var_department = StringVar()
        self.var_year = StringVar()
        
        # Background Image
        img = Image.open(r"bg.jpg")  # Add your background image
        img = img.resize((1530, 790), Image.Resampling.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img)
        
        bg_img = Label(self.root, image=self.photoimg)
        bg_img.place(x=0, y=0, width=1530, height=790)
        
        # Title
        title_lbl = Label(bg_img, text="FACE RECOGNITION ATTENDANCE SYSTEM", 
                         font=("times new roman", 35, "bold"), bg="white", fg="red")
        title_lbl.place(x=0, y=0, width=1300, height=45)
        
        # Main Frame
        main_frame = Frame(bg_img, bd=2, bg="white")
        main_frame.place(x=10, y=55, width=1200, height=600)
        
        # Left Frame
        left_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE, 
                                text="Student Details", font=("times new roman", 12, "bold"))
        left_frame.place(x=10, y=10, width=580, height=580)
        
        # Student Information
        # Student ID
        lbl_student_id = Label(left_frame, text="Student ID:", font=("times new roman", 12, "bold"), bg="white")
        lbl_student_id.grid(row=0, column=0, padx=10, pady=5, sticky=W)
        
        student_id_entry = ttk.Entry(left_frame, textvariable=self.var_student_id, 
                                     width=20, font=("times new roman", 12, "bold"))
        student_id_entry.grid(row=0, column=1, padx=10, pady=5, sticky=W)
        
        # Student Name
        lbl_student_name = Label(left_frame, text="Student Name:", font=("times new roman", 12, "bold"), bg="white")
        lbl_student_name.grid(row=1, column=0, padx=10, pady=5, sticky=W)
        
        student_name_entry = ttk.Entry(left_frame, textvariable=self.var_student_name, 
                                       width=20, font=("times new roman", 12, "bold"))
        student_name_entry.grid(row=1, column=1, padx=10, pady=5, sticky=W)
        
        # Department
        lbl_department = Label(left_frame, text="Department:", font=("times new roman", 12, "bold"), bg="white")
        lbl_department.grid(row=2, column=0, padx=10, pady=5, sticky=W)
        
        department_combo = ttk.Combobox(left_frame, textvariable=self.var_department, 
                                        font=("times new roman", 12, "bold"), width=18, state="readonly")
        department_combo["values"] = ("Computer Science", "Information Technology", "Electronics", "Mechanical")
        department_combo.current(0)
        department_combo.grid(row=2, column=1, padx=10, pady=5, sticky=W)
        
        # Year
        lbl_year = Label(left_frame, text="Year:", font=("times new roman", 12, "bold"), bg="white")
        lbl_year.grid(row=3, column=0, padx=10, pady=5, sticky=W)
        
        year_combo = ttk.Combobox(left_frame, textvariable=self.var_year, 
                                  font=("times new roman", 12, "bold"), width=18, state="readonly")
        year_combo["values"] = ("1st Year", "2nd Year", "3rd Year", "4th Year")
        year_combo.current(0)
        year_combo.grid(row=3, column=1, padx=10, pady=5, sticky=W)
        
        # Buttons Frame
        btn_frame = Frame(left_frame, bd=2, bg="white", relief=RIDGE)
        btn_frame.place(x=10, y=200, width=550, height=150)
        
        # Buttons
        take_photo_btn = Button(btn_frame, text="Take Photo Sample", command=self.take_photo, 
                                font=("times new roman", 13, "bold"), bg="blue", fg="white", width=15)
        take_photo_btn.grid(row=0, column=0, padx=10, pady=10)
        
        train_btn = Button(btn_frame, text="Train Data", command=self.train_data, 
                          font=("times new roman", 13, "bold"), bg="green", fg="white", width=15)
        train_btn.grid(row=0, column=1, padx=10, pady=10)
        
        recognize_btn = Button(btn_frame, text="Mark Attendance", command=self.mark_attendance, 
                              font=("times new roman", 13, "bold"), bg="orange", fg="white", width=15)
        recognize_btn.grid(row=1, column=0, padx=10, pady=10)
        
        export_btn = Button(btn_frame, text="Export Attendance", command=self.export_attendance, 
                           font=("times new roman", 13, "bold"), bg="purple", fg="white", width=15)
        export_btn.grid(row=1, column=1, padx=10, pady=10)
        
        # Right Frame
        right_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE, 
                                 text="Attendance Details", font=("times new roman", 12, "bold"))
        right_frame.place(x=600, y=10, width=580, height=580)
        
        # Table Frame
        table_frame = Frame(right_frame, bd=2, bg="white", relief=RIDGE)
        table_frame.place(x=10, y=10, width=550, height=550)
        
        # Scrollbar
        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)
        
        # Attendance Table
        self.attendance_table = ttk.Treeview(table_frame, columns=("id", "name", "dept", "year", "time", "status"),
                                             xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        
        scroll_x.config(command=self.attendance_table.xview)
        scroll_y.config(command=self.attendance_table.yview)
        
        # Table Headings
        self.attendance_table.heading("id", text="Student ID")
        self.attendance_table.heading("name", text="Name")
        self.attendance_table.heading("dept", text="Department")
        self.attendance_table.heading("year", text="Year")
        self.attendance_table.heading("time", text="Time")
        self.attendance_table.heading("status", text="Status")
        
        self.attendance_table["show"] = "headings"
        
        # Column Widths
        self.attendance_table.column("id", width=100)
        self.attendance_table.column("name", width=150)
        self.attendance_table.column("dept", width=120)
        self.attendance_table.column("year", width=100)
        self.attendance_table.column("time", width=150)
        self.attendance_table.column("status", width=100)
        
        self.attendance_table.pack(fill=BOTH, expand=1)
        
        # Initialize database and load attendance
        self.db = DatabaseHandler()
        self.load_attendance_data()
    
    def take_photo(self):
        """Capture face photos for training"""
        if self.var_student_id.get() == "" or self.var_student_name.get() == "":
            messagebox.showerror("Error", "Please enter Student ID and Name")
            return
        
        # Create dataset directory if not exists
        if not os.path.exists("dataset"):
            os.makedirs("dataset")
        
        # Initialize camera
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        cap = cv2.VideoCapture(0)
        
        sample_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            
            for (x, y, w, h) in faces:
                sample_count += 1
                
                # Save face image
                cv2.imwrite(f"dataset/User.{self.var_student_id.get()}.{sample_count}.jpg", 
                           gray[y:y+h, x:x+w])
                
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.waitKey(100)
            
            cv2.putText(frame, f"Taking Samples: {sample_count}/50", (50, 50), 
                       cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow("Taking Photos", frame)
            
            if sample_count >= 50 or cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
        messagebox.showinfo("Success", f"50 samples taken for {self.var_student_name.get()}")
    
    def train_data(self):
        """Train the face recognition model"""
        from face_trainer import FaceTrainer
        trainer = FaceTrainer()
        trainer.train_faces()
        messagebox.showinfo("Success", "Model trained successfully!")
    
    def mark_attendance(self):
        """Mark attendance using face recognition"""
        from face_recognizer import FaceRecognizer
        recognizer = FaceRecognizer()
        
        # Start recognition in a separate thread
        thread = threading.Thread(target=recognizer.recognize_faces, args=(self,))
        thread.daemon = True
        thread.start()
    
    def add_attendance_record(self, student_id, name, department, year):
        """Add attendance record to table"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Check if already marked today
        today = datetime.now().strftime("%Y-%m-%d")
        for item in self.attendance_table.get_children():
            values = self.attendance_table.item(item)["values"]
            if values[0] == student_id and today in values[4]:
                return False
        
        # Add to table
        self.attendance_table.insert("", "end", values=(student_id, name, department, year, current_time, "Present"))
        
        # Save to database
        self.db.mark_attendance(student_id, name, department, year, current_time)
        
        return True
    
    def load_attendance_data(self):
        """Load attendance data from database"""
        # Clear existing data
        for row in self.attendance_table.get_children():
            self.attendance_table.delete(row)
        
        # Load from database
        records = self.db.get_today_attendance()
        for record in records:
            self.attendance_table.insert("", "end", values=record)
    
    def export_attendance(self):
        """Export attendance to CSV"""
        from attendance_manager import AttendanceManager
        manager = AttendanceManager()
        manager.export_to_csv()
        messagebox.showinfo("Success", "Attendance exported successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    obj = AttendanceSystem(root)
    root.mainloop()