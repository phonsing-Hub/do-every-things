import os
import cv2
import dlib
import time
import  json
import numpy as np
from pathlib import Path
from typing import List
from fastapi import UploadFile
from src.database.mysql import mycursor, mydb
from src.lib.Mqtt import PahoMQTT

class Face:
    def __init__(self):
        self.person_name = []
        self.person_img_encoding = []
        self.fx = 0.25
        self.fy = 0.25
        self.detector = dlib.get_frontal_face_detector() # Histogram of Oriented Gradients (HOG) ร่วมกับ Linear SVM (Support Vector Machine)
        #self.detector = dlib.cnn_face_detection_model_v1("src/models/mmod_human_face_detector.dat") # Convolutional Neural Networks (CNN)
        self.predictor = dlib.shape_predictor("src/models/shape_predictor_68_face_landmarks.dat")
        self.face_rec_model = dlib.face_recognition_model_v1("src/models/dlib_face_recognition_resnet_model_v1.dat")
        self.base_dir = Path("public")
        self.paho = PahoMQTT()
        self.paho.connect_mqtt()

    def get_data_encoding_db(self): 
        # ดึงข้อมูลการเข้ารหัสจากฐานข้อมูล
        mycursor.execute("SELECT name, image_encoding FROM CPE422.users")
        myresult = mycursor.fetchall()
        for data in myresult:
            if "image_encoding" in data and data["image_encoding"]:
                # แปลงการเข้ารหัสที่เก็บเป็น JSON เป็นรายการ numpy array
                data["image_encoding"] = json.loads(data["image_encoding"])
                # เพิ่มข้อมูลเข้ารหัสและชื่อเข้าไปในรายการ
                self.person_img_encoding.append(np.array(data["image_encoding"]))  # แปลงเป็น numpy array
                self.person_name.append(data["name"])
                
    def readImg_encoding_all(self, folder_path):
        for person_folder in os.listdir(folder_path):
            person_path = os.path.join(folder_path, person_folder)
            if os.path.isdir(person_path):
                # เก็บชื่อของแต่ละบุคคล
                self.person_name.append(person_folder)
                # เก็บ encoding ของทุกภาพในโฟลเดอร์บุคคลนี้
                encodings = []
                for img_file in os.listdir(person_path):
                    img_path = os.path.join(person_path, img_file)
                    img = cv2.imread(img_path)
                    if img is None:
                        print(f"Could not read {img_path}. Skipping.")
                        continue
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    faces = self.detector(gray)
                    if len(faces) > 0:
                        face = faces[0]
                        landmarks = self.predictor(gray, face)
                        encoding = np.array(
                            self.face_rec_model.compute_face_descriptor(img, landmarks)
                        )
                        encodings.append(encoding)
                    else:
                        print(f"No face detected in {img_path}. Skipping.")
                # คำนวณค่าเฉลี่ยของ encoding สำหรับบุคคลนี้และเก็บใน list
                if encodings:
                    avg_encoding = np.mean(encodings, axis=0)
                    self.person_img_encoding.append(avg_encoding)
                else:
                    print(f"No encodings for {person_folder}. Skipping.")
    
    async def readImg_encoding(self, folder_path, name, note):
        encodings = []  # สำหรับเก็บ encoding ของแต่ละภาพ
        imagename = []
        # เก็บชื่อของบุคคล
        print(f"Processing folder: {folder_path}")
        # อ่านไฟล์ภาพในโฟลเดอร์
        for img_file in os.listdir(folder_path):
            img_path = os.path.join(folder_path, img_file)
            img = cv2.imread(img_path)
            if img is None:
                print(f"Could not read {img_path}. Skipping.")
                continue
            imagename.append(img_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.detector(gray)

            if len(faces) > 0:
                face = faces[0]
                landmarks = self.predictor(gray, face)
                encoding = np.array(
                    self.face_rec_model.compute_face_descriptor(img, landmarks)
                )
                encodings.append(encoding)
            else:
                print(f"No face detected in {img_path}. Skipping.")

        # คำนวณค่าเฉลี่ยของ encoding สำหรับบุคคลนี้และเก็บใน list
        if encodings:
            avg_encoding = np.mean(encodings, axis=0)
            encoding_json = json.dumps(avg_encoding.tolist())
            image_json = json.dumps(imagename)
            insert_query = (
                "INSERT INTO CPE422.users (name, note, image_encoding, image_name) VALUES (%s,%s,%s,%s)"
            )
            val = (name, note, encoding_json,image_json )
            mycursor.execute(insert_query, val)
            mydb.commit()
            return True
        else:
            print(f"No encodings found for {folder_path}. Skipping.")
            return False

    async def saveImage(self, name: str, images: List[UploadFile]):
        user_dir = self.base_dir / name
        user_dir.mkdir(parents=True, exist_ok=True)

        # Count existing images in the folder with a similar name pattern
        existing_images = len(list(user_dir.glob("img*")))

        for index, image in enumerate(images):
            extension = Path(image.filename).suffix

            # Use index + existing image count to avoid overwriting
            new_filename = f"img{index + existing_images}{extension}"
            image_path = user_dir / new_filename

            content = await image.read()
            with open(image_path, "wb") as f:
                f.write(content)

    def open(self):
        global cap
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open camera.")
            exit()

        last_publish_time = 0  # เวลาการส่งล่าสุด
        publish_interval = 5  # ระยะห่างการส่งในวินาที

        while True:
            start_time = time.time()
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame.")
                break

            frame = cv2.resize(frame, (1280, 720))
            small_frame = cv2.resize(frame, (0, 0), fx=self.fx, fy=self.fy)
            gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
            faces = self.detector(gray)

            for face in faces:
                x, y, w, h = (int(face.left() * 4), int(face.top() * 4), int(face.width() * 4), int(face.height() * 4))
                landmarks = self.predictor(gray, face)

                for n in range(68):
                    lx = landmarks.part(n).x * 4
                    ly = landmarks.part(n).y * 4
                    cv2.circle(frame, (lx, ly), 2, (200, 40, 120), -1)

                encoding = np.array(self.face_rec_model.compute_face_descriptor(small_frame, landmarks))
                matches = [np.linalg.norm(encoding - person_encoding) for person_encoding in self.person_img_encoding]
                if matches:
                    best_match_index = np.argmin(matches)
                    threshold = 0.4
                    if matches[best_match_index] < threshold:
                        name = self.person_name[best_match_index]
                    else:
                        name = "Unknow"
                else:
                    name = "Unknow"

                # current_time = time.time()
                if name != "Unknow" and (start_time - last_publish_time > publish_interval):
                    self.paho.publish({"LED1": 1, "LED2": 0})
                    last_publish_time = start_time 
                    print(f"{start_time}: onled")

                color = (0, 0, 200) if name == "Unknow" else (200, 0, 0)
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.1, color, 2)

            end_time = time.time()
            fps = int(1 / (end_time - start_time))
            cv2.putText(frame, f"FPS: {fps}", (15, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (96, 18, 243), 3)

            _, buffer = cv2.imencode(".jpg", frame)
            frame_bytes = buffer.tobytes()
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"
            )

        cap.release()
        cv2.destroyAllWindows()

    def show_results(self):
        print("Person Names:", self.person_name)
        print("Person Image Encodings:", self.person_img_encoding)

