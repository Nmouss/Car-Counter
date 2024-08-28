-pip3 install ultralytics

import cv2
from ultralytics import YOLO

model = YOLO("yolov8n.pt")
results = model.track(source="/Users/nabilmouss/Desktop/ VEHICLE DETECTION/Test Video/Videoo.mp4", show=True, save=False, name='test_result', persist=True, classes=[2, 3, 5, 7]) # this is just taking the video 
