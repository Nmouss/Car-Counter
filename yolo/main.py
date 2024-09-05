import time
import cv2

from ultralytics import YOLO
from object_counter import ObjectCounter

model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture("/Path/to/your/directory/.mp4")
assert cap.isOpened(), "Error reading video file"
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

line_points = [(20, 400), (1080, 400)]  # line or region points
classes_to_count = [2, 3, 5, 7]  # person and car classes for count

# Init Object Counter
counter = ObjectCounter(
    view_img=True,
    reg_pts=line_points,
    names=model.names,
    draw_tracks=True,
    line_thickness=2,
)
current_time = time.strftime('%X') # current time


dictonary = []
Counter = 0
while cap.isOpened():
    success, im0 = cap.read()
    if not success:
        print("Video frame is empty or video processing has been successfully completed.")
        break
    tracks = model.track(im0, persist=True, show=False, classes=classes_to_count)

    if len(counter.count_ids) != Counter:
        Counter += 1
        dictonary.append(counter.is_vehicle)
    
    print(dictonary, counter.count_ids)

    im0 = counter.start_counting(im0, tracks)

print(dictonary, len(dictonary), len(counter.count_ids))
cap.release()

cv2.destroyAllWindows()
