# CAR COUNTER & SPEED ESTIMATION
## WHAT IS THIS?
As the name suggests this is an algorithm that I compiled by using open source code by ultralytics YoloV8 detection algorithm. I combined the estimated speed and car counting classes to create an algorithm that detects cars, their classification (car, truck, motorcycle, etc.), speed estimation (dependent heavily on GPU capabilities), and the time when the car was counted. I compiled all the data on an SQLite database for easy analysis using SQL.


![vehicle tracking](https://github.com/user-attachments/assets/78a4dc35-7b2e-412c-869e-cc781091f692)



## WHAT I LEARNED
Originally I wanted to use mediapipe to detect/ count cars however when I was compiling the model I encountered huge GPU usage to the point where the latency was so extreme that it would be insufficient to count the cars so I decided to do some reseach. Not only was the latency high but mediapipe was not accurate with its detections. Heres what I learned.
- YOLOv8 by Ultralytics optimizes for efficienty while trying to maintain a high mAP (mean average precision). YOLOv8s object detection architecture uses CNNs (Convolutional Neural Networks) like mediapipe however the difference being is that it uses a single unified CNN which does two tasks at once, find the objects location and classification. It uses feature pyramids and convolutional layers to extract multi scale features from images. I also found YOLOv8 easier to customize as compared to mediapipe. ![63c697fd4ef3d83d2e35a8c2_YOLO architecture-min](https://github.com/user-attachments/assets/db048a27-dc10-4453-9a72-c040da6f1b5a)
- Mediapipe by google is mainly used for real time posing, hand posing etc. Mediapipes object detection uses CNNs however the difference is that instead of using a single unified CNN it uses multiple models. There are multiple stages; detection, tracking, and refinement. These stages all use their own individual CNNs which together use a higher GPU consumption as compared to YOLOv8's single CNN architecture. Simple rule more calculations i.e dot product or activation functions, the higher the consumption. I also found it harder to customize mediapipe as the code was not well documented and not easier to decipher. 



# NOTES
This project is still under development. A few things that I want to accomplish:
- Better optimization! In order for me to track the counting and speed I am actually using two videos (Im hiding one) which is using twice the processing power. I think my solution is multi-threading rather than having two objects.
- I want to see if I can add my database to the cloud for safe storage rather than my disk.
- I want to see if I can further customize my models accuracy by introducing some of my own dataset of cars in my area. This will be time consuming as I will have to annotate every picture like I did for my time-management project but if I have the time I will.

# HELPFUL SOURCES
https://encord.com/blog/yolo-object-detection-guide/
