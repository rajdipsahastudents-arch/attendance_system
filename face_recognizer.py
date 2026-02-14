import cv2
import numpy as np
import os
import pickle
from datetime import datetime
import tkinter.messagebox as messagebox

class FaceRecognizer:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        
        # Load trained model if exists
        if os.path.exists('trainer/trainer.yml'):
            self.recognizer.read('trainer/trainer.yml')
        
        # Load student mapping
        self.student_mapping = {}
        if os.path.exists('trainer/student_mapping.pkl'):
            with open('trainer/student_mapping.pkl', 'rb') as f:
                self.student_mapping = pickle.load(f)
    
    def recognize_faces(self, app):
        """Real-time face recognition for attendance"""
        cap = cv2.VideoCapture(0)
        
        # Dictionary to track marked attendance
        marked_students = set()
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
            for (x, y, w, h) in faces:
                # Recognize face
                id, confidence = self.recognizer.predict(gray[y:y+h, x:x+w])
                
                # If confidence is good enough (lower is better for LBPH)
                if confidence < 100:
                    student_id = str(id)
                    student_name = self.student_mapping.get(student_id, f"Student_{student_id}")
                    
                    # Check if already marked today
                    if student_id not in marked_students:
                        # Mark attendance
                        marked = app.add_attendance_record(
                            student_id, 
                            student_name, 
                            "Computer Science",  # This should come from database
                            "3rd Year"           # This should come from database
                        )
                        
                        if marked:
                            marked_students.add(student_id)
                    
                    # Draw rectangle and name
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(frame, student_name, (x, y-10), 
                               cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 0), 2)
                    cv2.putText(frame, f"Confidence: {100-confidence:.1f}%", (x, y+h+20), 
                               cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 1)
                else:
                    # Unknown face
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                    cv2.putText(frame, "Unknown", (x, y-10), 
                               cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255), 2)
            
            cv2.putText(frame, f"Marked: {len(marked_students)} students", (10, 30), 
                       cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, "Press 'q' to quit", (10, 60), 
                       cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
            
            cv2.imshow("Face Recognition Attendance", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
        messagebox.showinfo("Attendance", f"Attendance marked for {len(marked_students)} students")

if __name__ == "__main__":
    recognizer = FaceRecognizer()
    # This would need the app instance to work properly