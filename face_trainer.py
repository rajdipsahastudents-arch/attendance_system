import cv2
import numpy as np
from PIL import Image
import os
import pickle

class FaceTrainer:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        
    def train_faces(self):
        """Train the face recognition model"""
        # Create trainer directory if not exists
        if not os.path.exists("trainer"):
            os.makedirs("trainer")
        
        # Get all face images
        path = 'dataset'
        
        if not os.path.exists(path):
            print("Dataset folder not found!")
            return
        
        image_paths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]
        faces = []
        ids = []
        
        for image_path in image_paths:
            try:
                # Convert to grayscale
                pil_image = Image.open(image_path).convert('L')
                image_np = np.array(pil_image, 'uint8')
                
                # Get ID from filename
                id = int(os.path.split(image_path)[-1].split(".")[1])
                
                # Detect face
                faces_detected = self.face_cascade.detectMultiScale(image_np)
                
                for (x, y, w, h) in faces_detected:
                    faces.append(image_np[y:y+h, x:x+w])
                    ids.append(id)
                    
            except Exception as e:
                print(f"Error processing {image_path}: {e}")
                continue
        
        if len(faces) == 0:
            print("No faces found for training!")
            return
        
        # Train the recognizer
        self.recognizer.train(faces, np.array(ids))
        
        # Save the trained model
        self.recognizer.write('trainer/trainer.yml')
        
        # Save student info mapping
        self.save_student_mapping()
        
        print(f"Training completed! {len(np.unique(ids))} students trained.")
    
    def save_student_mapping(self):
        """Save student ID to name mapping"""
        mapping = {}
        
        # Get all dataset images
        path = 'dataset'
        if os.path.exists(path):
            for filename in os.listdir(path):
                if filename.endswith('.jpg'):
                    try:
                        # Extract ID from filename (User.ID.sample.jpg)
                        parts = filename.split('.')
                        if len(parts) >= 2:
                            student_id = parts[1]
                            # We need to get student name from somewhere
                            # This could be stored in a database
                            mapping[student_id] = f"Student_{student_id}"
                    except:
                        continue
        
        # Save mapping
        with open('trainer/student_mapping.pkl', 'wb') as f:
            pickle.dump(mapping, f)

if __name__ == "__main__":
    trainer = FaceTrainer()
    trainer.train_faces()