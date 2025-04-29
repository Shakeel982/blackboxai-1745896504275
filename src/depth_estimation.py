import torch
import torchvision.transforms as transforms
from PIL import Image
import cv2
import numpy as np

class DepthEstimator:
    def __init__(self, model):
        self.model = model
        self.model.eval()
        self.transform = transforms.Compose([
            transforms.Resize((384, 384)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225]),
        ])

    def estimate_depth(self, frame):
        """
        Estimate depth map from a single frame.
        """
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        input_tensor = self.transform(img).unsqueeze(0)
        with torch.no_grad():
            depth = self.model(input_tensor)
        depth = torch.nn.functional.interpolate(
            depth.unsqueeze(1),
            size=frame.shape[:2],
            mode="bicubic",
            align_corners=False,
        ).squeeze().cpu().numpy()
        depth_min = depth.min()
        depth_max = depth.max()
        depth_normalized = (depth - depth_min) / (depth_max - depth_min)
        return depth_normalized
