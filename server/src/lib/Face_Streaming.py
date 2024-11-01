import os
import cv2
import dlib
import time
import  json
import numpy as np
from src.database.mysql import mycursor

class Stream:
    def __init__(self):
        self.person_name = []
        self.person_img_encoding = []
        self.fx = 0.25
        self.fy = 0.25
        self.detector = dlib.get_frontal_face_detector() # Histogram of Oriented Gradients (HOG) ร่วมกับ Linear SVM (Support Vector Machine)
        #self.detector = dlib.cnn_face_detection_model_v1("src/models/mmod_human_face_detector.dat") # Convolutional Neural Networks (CNN)
        self.predictor = dlib.shape_predictor("src/models/shape_predictor_68_face_landmarks.dat")
        self.face_rec_model = dlib.face_recognition_model_v1("src/models/dlib_face_recognition_resnet_model_v1.dat")
        

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
    
    def readImg_encoding(self, folder_path, name):
        encodings = []  # สำหรับเก็บ encoding ของแต่ละภาพ
        # เก็บชื่อของบุคคล
        print(f"Processing folder: {folder_path}")
        # อ่านไฟล์ภาพในโฟลเดอร์
        for img_file in os.listdir(folder_path):
            img_path = os.path.join(folder_path, img_file)
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
            self.person_name.append(name)
            print(f"Average encoding for {folder_path}: {avg_encoding}")
        else:
            print(f"No encodings found for {folder_path}. Skipping.")

    def open(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open camera.")
            exit()

        while True:
            start_time = time.time()  # เริ่มจับเวลา
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame.")
                break

            small_frame = cv2.resize(frame, (0, 0), fx=self.fx, fy=self.fy)
            gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
            faces = self.detector(gray)

            for face in faces:
                # ตีกรอบสี่เหลี่ยมรอบใบหน้า get_frontal_face_detector()
                x, y, w, h = (int(face.left() * 4), int(face.top() * 4), int(face.width() * 4), int(face.height() * 4))
                # ตีกรอบสี่เหลี่ยมรอบใบหน้า mmod_human_face_detector.dat cnn 
                # x, y, w, h = (
                #     face.rect.left() * 4,
                #     face.rect.top() * 4,
                #     (face.rect.right() - face.rect.left()) * 4,
                #     (face.rect.bottom() - face.rect.top()) * 4,
                # )

                cv2.rectangle(frame, (x, y), (x + w, y + h), (238, 111, 0), 2)
                # ตรวจจับจุด landmark บนใบหน้า
                landmarks = self.predictor(gray, face) # cnn use face.rect
                for n in range(68):
                    lx = landmarks.part(n).x *4
                    ly = landmarks.part(n).y *4
                    cv2.circle(frame, (lx, ly), 2, (200, 40, 120), -1)

                encoding = np.array(self.face_rec_model.compute_face_descriptor(small_frame, landmarks))
                # ตรวจสอบว่าตรงกับใครใน self.person_img_encoding หรือไม่
                matches = [np.linalg.norm(encoding - person_encoding) for person_encoding in self.person_img_encoding]
                if matches:
                    best_match_index = np.argmin(matches)
                    threshold = 0.5  # ค่าธรณีที่ใช้ในการตัดสินใจว่าตรงกันหรือไม่
                    if matches[best_match_index] < threshold:
                        name = self.person_name[best_match_index]
                    else: 
                        name = "Unknow"
                else: 
                    name = "Unknow"

                # แสดงชื่อบุคคลในวิดีโอ
                cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (238, 111, 0), 2)
            # คำนวณ FPS
            end_time = time.time()
            fps = int(1 / (end_time - start_time))
            # แสดงค่า FPS บนเฟรม
            cv2.putText(frame,f"FPS: {fps}", (15, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (96, 18, 243), 3)
            cv2.imshow("VideoCapture: 0", frame)
            key = cv2.waitKey(1)
            if key == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()

    def show_results(self):
        print("Person Names:", self.person_name)
        print("Person Image Encodings:", self.person_img_encoding)
