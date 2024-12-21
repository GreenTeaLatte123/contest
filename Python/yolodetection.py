import cv2
import firebase_admin
import time
import os
from firebase_admin import credentials, storage
from ultralytics import YOLO

# Firebase 서비스 계정 키 경로
cred = credentials.Certificate("D:/yolov8/raspberrykey.json")

# Firebase 프로젝트 초기화
firebase_admin.initialize_app(cred, {
    "storageBucket": "raspberry-b22a0.appspot.com"
})

# YOLOv8 모델 로드
model = YOLO('D:/yolov8/best.pt')

# 비디오 파일 열기
video_path = 'http://192.168.137.103:8081/?action=stream'
cap = cv2.VideoCapture(video_path)

# 로컬에 저장할 파일명
timestamp = time.strftime("%Y%m%d%H%M%S")
d_drive_folder = 'D:/videos/'

local_filename = os.path.join(d_drive_folder, f'output_video_{timestamp}.avi')

# Firebase Storage에 저장할 파일명
storage_filename = f"video_{timestamp}.avi"

# Firebase Storage에 비디오 업로드
storage_client = storage.bucket()

# 비디오 저장 설정
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(local_filename, fourcc, 20.0, (640, 480))

# 비디오 프레임 반복 처리
while cap.isOpened():
    # 비디오에서 프레임 읽기
    success, frame = cap.read()

    if success:
        # YOLOv8 추론 실행
        results = model(frame)

        # 결과를 프레임에 시각화
        annotated_frame = results[0].plot()
        
        # 로컬에 프레임 저장
        out.write(annotated_frame)
        
        # 시각화된 프레임 표시
        cv2.imshow("YOLOv8 Inference", annotated_frame)

        # 'q' 키가 눌리면 루프 종료
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # 비디오 끝에 도달하면 루프 종료
        break

# 로컬에 저장된 비디오 파일을 Firebase Storage에 업로드
blob = storage_client.blob('videos/' + storage_filename)
blob.upload_from_filename(local_filename)
print(f"{storage_filename} upload success")

# 비디오 캡처 객체 해제
cap.release()
out.release()
cv2.destroyAllWindows()