import cv2
import mediapipe as mp
import pandas as pd
import uuid
from posture_score import calculate_posture_score
import os

def generate_normal_report(video_path, student_ids):
    mp_pose = mp.solutions.pose
    posture_scores = {student: 0 for student in student_ids}
    total_frames = 0

    cap = cv2.VideoCapture(video_path)
    with mp_pose.Pose() as pose:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            total_frames += 1

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(frame_rgb)

            if results.pose_landmarks:
                # Simulate good posture if head and shoulders are aligned (basic check)
                landmarks = results.pose_landmarks.landmark
                left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y
                right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y
                head = landmarks[mp_pose.PoseLandmark.NOSE.value].y

                posture_quality = 1.0 if abs(left_shoulder - right_shoulder) < 0.05 and head < left_shoulder else 0.5

                for student in posture_scores:
                    posture_scores[student] += posture_quality

    cap.release()

    for student in posture_scores:
        posture_scores[student] = round((posture_scores[student] / total_frames) * 100, 2)

    df = pd.DataFrame({
        'Student ID': student_ids,
        'Attentiveness Score (%)': [posture_scores.get(sid, 0) for sid in student_ids]
    })

    filename = f"reports/Normal_Attentiveness_Report_{uuid.uuid4().hex[:8]}.xlsx"
    df.to_excel(filename, index=False)
    return filename
