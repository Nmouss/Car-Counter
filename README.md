# CAR COUNTER & SPEED ESTIMATION
## WHAT IS THIS?
As the name suggests this is an algorithm that I compiled by using open source code by ultralytics YoloV8 detection algorithm. I combined the estimated speed and car counting classes to create an algorithm that detects cars, their classification (car, truck, motorcycle, etc.), speed estimation (dependent heavily on GPU capabilities), and the time when the car was counted. I compiled all the data on an SQLite database for easy analysis using SQL.


![vehicle tracking](https://github.com/user-attachments/assets/78a4dc35-7b2e-412c-869e-cc781091f692)



## WHAT I LEARNED
Originally I wanted to use mediapipe to detect/ count cars however when I was compiling the model I encountered huge GPU usage to the point where the latency was so extreme that it would be insufficient to count the cars so I decided to do some reseach. Not only was the latency high but mediapipe was not accurate with its detections. Heres what I learned.
- YOLOv8 by Ultralytics optimizes for efficienty while trying to maintain a high mAP (mean average precision). YOLOv8s object detection architecture uses CNNs (Convolutional Neural Networks) however the difference being is that it uses a single unified CNN which does two tasks at once, find the objects location and classification. It uses feature pyramids and convolutional layers to extract multi-scale features from images. ![63c697fd4ef3d83d2e35a8c2_YOLO architecture-min](https://github.com/user-attachments/assets/db048a27-dc10-4453-9a72-c040da6f1b5a)


# HELPFUL SOURCES
https://encord.com/blog/yolo-object-detection-guide/

