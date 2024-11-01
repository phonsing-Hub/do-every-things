import cv2
import dlib
import numpy as np

# โหลดโมเดลตรวจจับใบหน้าและจุด landmark
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("src/models/shape_predictor_68_face_landmarks.dat")
face_rec_model = dlib.face_recognition_model_v1("src/models/dlib_face_recognition_resnet_model_v1.dat")

def get_face_encoding_and_landmarks(image_path):
    # อ่านภาพ
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # ตรวจจับใบหน้าในภาพ
    faces = detector(gray)

    if len(faces) == 0:
        print(f"No face detected in {image_path}")
        return None, img

    for face in faces:
        # ตีกอบสี่เหลี่ยมรอบใบหน้า
        x, y, w, h = face.left() - 2, face.top() - 2, face.width() + 4, face.height() + 4
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        # ตรวจจับจุด landmark บนใบหน้า
        landmarks = predictor(gray, face)

        # วาดจุด landmark บนใบหน้า (68 จุด)
        for n in range(68):
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            cv2.circle(img, (x, y), 2, (0, 255, 0), -1)

        # สร้าง Face Encoding โดยใช้เวกเตอร์ 128 ค่า
        encoding = np.array(face_rec_model.compute_face_descriptor(img, landmarks))
        return encoding, img

# กำหนดพาธสำหรับภาพสองใบหน้า
face_A_path = "src/images/9arm1.jpg"  # ใบหน้า A
face_B_path = "src/images/9arm2.webp"  # ใบหน้า B

# รับ Face Encoding และภาพพร้อม landmarks สำหรับทั้งสองใบหน้า
encoding_A, img_A = get_face_encoding_and_landmarks(face_A_path)
encoding_B, img_B = get_face_encoding_and_landmarks(face_B_path)

if encoding_A is not None and encoding_B is not None:
    # เปรียบเทียบ Face Encoding
    distance = np.linalg.norm(encoding_A - encoding_B)
    threshold = 0.6  # ระยะทางที่ตั้งไว้เพื่อพิจารณาว่าใบหน้าตรงกัน

    if distance < threshold:
        print("Faces match!")
    else:
        print("Faces do not match.")

# แสดงภาพของใบหน้า A พร้อม landmarks
while True:
    cv2.imshow("Face A with Landmarks", img_A)
    cv2.imshow("Face B with Landmarks", img_B)
    key = cv2.waitKey(1)
    if key == ord('q'):
            break
    
cv2.destroyAllWindows()