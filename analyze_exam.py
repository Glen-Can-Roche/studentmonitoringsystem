import cv2
import mediapipe as mp
import pandas as pd
import uuid

def generate_exam_report(video_path, student_ids):
    mp_pose = mp.solutions.pose
    movement_scores = {student: 0 for student in student_ids}
    total_frames = 0

    cap = cv2.VideoCapture(video_path)
    previous_landmarks = None

    with mp_pose.Pose() as pose:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            total_frames += 1

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(frame_rgb)

            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                if previous_landmarks:
                    movement = sum(abs(lm1.x - lm2.x) + abs(lm1.y - lm2.y)
                                   for lm1, lm2 in zip(landmarks, previous_landmarks)) / len(landmarks)
                    cheating_probability = 1.0 if movement > 0.03 else 0.1
                else:
                    cheating_probability = 0.1

                for student in movement_scores:
                    movement_scores[student] += cheating_probability

                previous_landmarks = landmarks

    cap.release()

    for student in movement_scores:
        score = movement_scores[student] / total_frames
        movement_scores[student] = min(round(score * 100, 2), 100)

    df = pd.DataFrame({
        'Student ID': student_ids,
        'Cheating Probability (%)': [movement_scores.get(sid, 0) for sid in student_ids]
    })

    filename = f"reports/Exam_Cheating_Report_{uuid.uuid4().hex[:8]}.xlsx"
    df.to_excel(filename, index=False)
    return filename
