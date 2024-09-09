import time
import cv2
from ultralytics import YOLO
from object_counter import ObjectCounter
from speed_estimation import SpeedEstimator
import sqlite3

model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture("/PATH/TO/YOUR/DIRECTORY/VIDEO.mp4")
assert cap.isOpened(), "Error reading video file"
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

print("width of video: ", w, "height of video: ", h)

line_points = [(20, 400), (1080, 400)]  # line / region points (2points = line ofc), modify this for your detection needs
classes_to_count = [2, 3, 5, 7]  # car, truck, motorcycle, bus; classes to count

# Initializes the database and connects to it
connection = sqlite3.connect("vehicle_information.db")
cursor = connection.cursor()

# Deletion of previous data
cursor.execute("DELETE FROM vehicle_data") 
cursor.execute("DELETE FROM sqlite_sequence WHERE name='vehicle_data'") 

# Creates columns 'id, vehicle_type, speed, time', rows which contain the data type TEXT for 
cursor.execute('''
    CREATE TABLE IF NOT EXISTS vehicle_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vehicle_type TEXT,
        speed_in_MPH REAL,
        time TEXT
    )
''')

# Video writer
# video_writer = cv2.VideoWriter("object_counting_output.avi", cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h)) # If I want to save the video

# Init Object Counter
counter = ObjectCounter(
    view_img=True,
    reg_pts=line_points,
    names=model.names,
    draw_tracks=True,
    line_thickness=2,
)

# speed approximator object
speed_obj = SpeedEstimator(
    reg_pts=line_points,
    names=model.model.names,
    view_img=False,
)

vehicle_type = []
speeds = []
Counter = 0
id_numbers = counter.count_ids
dictonary_of_speed = speed_obj.dist_data

while cap.isOpened():
    current_time = time.strftime('%X') # current time in military time
    success, im0 = cap.read()
    if not success:
        print("Video frame is empty or video processing has been successfully completed.")
        break

    # this tracks the objects
    tracks = model.track(im0, persist=True, show=False)
    
    if len(dictonary_of_speed) > Counter and len(id_numbers) > Counter:
        Counter += 1
        vehicle_type.append(counter.is_vehicle)
        
        speeds.append(dictonary_of_speed[id_numbers[-1]])

        if vehicle_type[-1] == "train":
            vehicle_type[-1] = "truck"

        cursor.execute('''
            INSERT INTO vehicle_data (vehicle_type, speed_in_MPH, time)
            VALUES (?, ?, ?)
        ''', (vehicle_type[-1], float(dictonary_of_speed[id_numbers[-1]]) * 0.621371, current_time))

        connection.commit()

    speed_obj.estimate_speed(im0, tracks) # this messes everything up

    counter.start_counting(im0, tracks)

    # Estimates speed and updates the data
    id_numbers = counter.count_ids
    dictonary_of_speed = speed_obj.dist_data

    # video_writer.write(im0)
# print(vehicle_type, len(vehicle_type), len(counter.count_ids), speeds)

cap.release()
# video_writer.release()
cv2.destroyAllWindows()
connection.close()
