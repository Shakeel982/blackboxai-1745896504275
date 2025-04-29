import mediapipe as mp
import cv2
import numpy as np

mp_pose = mp.solutions.pose

class PoseEstimator:
    def __init__(self, static_image_mode=False, model_complexity=2, enable_segmentation=False, min_detection_confidence=0.5):
        self.pose = mp_pose.Pose(static_image_mode=static_image_mode,
                                 model_complexity=model_complexity,
                                 enable_segmentation=enable_segmentation,
                                 min_detection_confidence=min_detection_confidence)

    def estimate_pose(self, image):
        """
        Estimate 3D pose landmarks from an image.
        Returns normalized landmarks or None if no pose detected.
        """
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.pose.process(image_rgb)
        if results.pose_landmarks:
            return results.pose_landmarks.landmark
        else:
            return None

    def draw_landmarks(self, image, landmarks):
        """
        Draw pose landmarks on the image.
        """
        mp.solutions.drawing_utils.draw_landmarks(
            image, landmarks, mp_pose.POSE_CONNECTIONS)
        return image
