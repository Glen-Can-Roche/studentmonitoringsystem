import face_recognition
import cv2
import os

def load_known_faces(dataset_path='dataset'):
    known_encodings = []
    student_ids = []
    for filename in os.listdir(dataset_path):
        if filename.endswith(('.jpg', '.png')):
            img_path = os.path.join(dataset_path, filename)
            image = face_recognition.load_image_file(img_path)
            encoding = face_recognition.face_encodings(image)
            if encoding:
                known_encodings.append(encoding[0])
                student_ids.append(os.path.splitext(filename)[0])
    return known_encodings, student_ids

def mark_attendance(video_path):
    video = cv2.VideoCapture(video_path)
    known_encodings, student_ids = load_known_faces()
    present_students = set()

    while True:
        ret, frame = video.read()
        if not ret:
            break

        small = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)
        locations = face_recognition.face_locations(rgb)
        encodings = face_recognition.face_encodings(rgb, locations)

        for encode in encodings:
            matches = face_recognition.compare_faces(known_encodings, encode)
            for i, match in enumerate(matches):
                if match:
                    present_students.add(student_ids[i])

    video.release()
    return list(present_students)
