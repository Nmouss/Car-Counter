-pip3 install ultralytics

import cv2

from ultralytics import YOLO, solutions

# from shapely import Polygon

# model = YOLO("yolov8n.pt")
# results = model.track(source="/Users/nabilmouss/Desktop/ VEHICLE DETECTION/Test Video/Videoo.mp4", show=True, save=False, name='test_result', persist=True, classes=[2, 3, 5, 7]) # this is just taking the video 


# Load the pre-trained YOLOv8 model
model = YOLO("yolov8n.pt")

# Open the video file
cap = cv2.VideoCapture("/PATH/TO/YOUR/DIRECTORY/VIDEO.mp4")
assert cap.isOpened(), "Error reading video file"

# Get video properties: width, height, and frames per second (fps)
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

print(w, h)
# Define points for a line or region of interest in the video frame
#line_points = [(0, 300), (3840, 300)]  # Line coordinates
line_points = [(20, 400), (3840, 404), (3840, 360), (20, 360)]
# Specify classes to count, for example: person (0) and car (2)
classes_to_count = [2, 3, 5, 7]  # Class IDs for car, truck, motorcycle, bus

# Initialize the video writer to save the output video
# video_writer = cv2.VideoWriter("object_counting_output.mp4", cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

# Initialize the Object Counter with visualization options and other parameters
counter = solutions.ObjectCounter(
    view_img=True,  # Display the image during processing
    reg_pts=line_points,  # Region of interest points
    names=model.names,  # Class names from the YOLO model
    draw_tracks=True,  # Draw tracking lines for objects
    line_thickness=2,  # Thickness of the lines drawn
)
dictonary = {}
# Process video frames in a loop
while cap.isOpened():
    success, im0 = cap.read()
    if not success:
        print("Video frame is empty or video processing has been successfully completed.")
        break

    # Perform object tracking on the current frame, filtering by specified classes
    tracks = model.track(im0, persist=True, show=False, classes=classes_to_count)

    # Use the Object Counter to count objects in the frame and get the annotated image
    im0 = counter.start_counting(im0, tracks)

    # Write the annotated frame to the output video
    # video_writer.write(im0)
    print(im0)
# Release the video capture and writer objects
cap.release()
# video_writer.release()

# Close all OpenCV windows
cv2.destroyAllWindows()
