import cv2
import dlib

# โหลดโมเดลตรวจจับใบหน้าและจุด landmark
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
face_rec_model = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# กำหนด codec และสร้าง VideoWriter สำหรับบันทึกวิดีโอ
# fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # สำหรับ MP4
# out = cv2.VideoWriter('output.mp4', fourcc, 30.0, (640, 480))

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    for face in faces:
        # ตรวจจับจุด landmark บนใบหน้า
        landmarks = predictor(gray, face)

        # วาดจุด landmark บนใบหน้า (68 จุด)
        for n in range(68):
            x = landmarks.part(n).x * 4  # ขยายขนาดกลับ
            y = landmarks.part(n).y * 4
            cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

    #out.write(frame)  # บันทึกเฟรมลงในวิดีโอ
    cv2.imshow("VideoCapture: 0", frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
#out.release()
cv2.destroyAllWindows()