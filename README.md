# CAR COUNTER & SPEED ESTIMATION
## WHAT IS THIS?
As the name suggests this is an algorithm that I compiled by using open source code by ultralytics YoloV8 detection algorithm. I combined the estimated speed and car counting classes to create an algorithm that detects cars, their classification (car, truck, motorcycle, etc.), speed estimation (dependent heavily on GPU capabilities), and the time when the car was counted. I compiled all the data on an SQLite database for easy analysis using SQL.


![vehicle tracking](https://github.com/user-attachments/assets/78a4dc35-7b2e-412c-869e-cc781091f692)



## WHAT I LEARNED
Originally I wanted to use mediapipe to detect/ count cars however when I was compiling the model I encountered huge GPU usage to the point where the latency was so extreme that it would be insufficient to count the cars so I decided to do some reseach. Not only was the latency high but mediapipe was not accurate with its detections.

