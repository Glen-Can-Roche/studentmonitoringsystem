# posture_score.py

def calculate_posture_score(landmarks):
    """
    Calculate a posture score based on shoulder and hip alignment.

    Parameters:
    - landmarks: A list of 33 pose landmarks from MediaPipe

    Returns:
    - posture_score: A float value between 0 and 1 representing attentiveness
    """
    # Indices for key landmarks in MediaPipe
    LEFT_SHOULDER = 11
    RIGHT_SHOULDER = 12
    LEFT_HIP = 23
    RIGHT_HIP = 24

    try:
        left_shoulder = landmarks[LEFT_SHOULDER]
        right_shoulder = landmarks[RIGHT_SHOULDER]
        left_hip = landmarks[LEFT_HIP]
        right_hip = landmarks[RIGHT_HIP]

        # Calculate vertical distances (Y-axis)
        left_vertical = abs(left_shoulder.y - left_hip.y)
        right_vertical = abs(right_shoulder.y - right_hip.y)

        # Average vertical distance
        average_vertical = (left_vertical + right_vertical) / 2

        # Posture score: upright posture ~ larger vertical difference
        # Score clipped between 0.3 and 1.0 to avoid extreme values
        posture_score = min(max(average_vertical / 0.5, 0.3), 1.0)
        return round(posture_score, 2)

    except Exception as e:
        print(f"Posture score calculation failed: {e}")
        return 0.0
