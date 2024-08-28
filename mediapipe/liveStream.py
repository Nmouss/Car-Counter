import cv2
import yt_dlp # Imports for webscrapping

import argparse
import sys
import time

import cv2
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from utils import visualize

COUNTER, FPS = 0, 0
START_TIME = time.time()

def run(model: str, max_results: int, score_threshold: float, 
        camera_id: int, width: int, height: int, category_allowlist: list) -> None:
    
    def get_video_url(youtube_url):
        ydl_opts = {
            'format': 'best',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=False)
            video_url = info_dict['url']
        return video_url
    
    def save_result(result: vision.ObjectDetectorResult, unused_output_image: mp.Image, timestamp_ms: int):
        global FPS, COUNTER, START_TIME

        """# Calculate the FPS
        if COUNTER % fps_avg_frame_count == 0:
            FPS = fps_avg_frame_count / (time.time() - START_TIME)
            START_TIME = time.time()"""
        detection_result_list.append(result)
        COUNTER += 1
    
    base_options = python.BaseOptions(model_asset_path=model)
    options = vision.ObjectDetectorOptions(
        base_options=base_options,
        running_mode=vision.RunningMode.LIVE_STREAM,
        max_results=max_results,
        score_threshold=score_threshold,
        category_allowlist=category_allowlist,  # Add category_allowlist here
        result_callback=save_result
    )
    detector = vision.ObjectDetector.create_from_options(options)

    row_size = 50  # pixels
    left_margin = 24  # pixels
    text_color = (0, 0, 0)  # black
    font_size = 1
    font_thickness = 1
    fps_avg_frame_count = 10

    detection_frame = None
    detection_result_list = []

    global Score
    Score = 0

    # Original embedded YouTube URL
    embedded_url = input("What is the youtube live stream url? ")
    if "/embed/" in embedded_url:
    # Extract the video ID from the embedded URL
        video_id = embedded_url.split('/embed/')[1].split('?')[0]
        youtube_url = f"https://www.youtube.com/watch?v={video_id}"
    else:
        youtube_url = embedded_url
    # Convert to standard YouTube URL

    # Get the direct video URL
    video_url = get_video_url(youtube_url)

    # Open the video stream using OpenCV
    capture = cv2.VideoCapture(video_url)


    if not capture.isOpened():
        print("Error: Unable to open video stream")
    else:
        while True:
            # Capture frame-by-frame
            grabbed, frame = capture.read()

            if not grabbed:
                print("Error: Frame not grabbed")
                break

            image = cv2.flip(frame, 1)

            # Convert the image from BGR to RGB as required by the TFLite model.
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)

            # Run object detection using the model.
            detector.detect_async(mp_image, time.time_ns() // 1000)
            
            # Show the FPS
            fps_text = 'FPS = {:.1f}'.format(FPS)
            text_location = (left_margin, row_size)
            current_frame = image
            cv2.putText(current_frame, fps_text, text_location, cv2.FONT_HERSHEY_DUPLEX,
                        font_size, text_color, font_thickness, cv2.LINE_AA)
            
            # if the detection result list has something
            if detection_result_list:
                current_frame, result = visualize(current_frame, detection_result_list[0])
                # print(result) # here result is the actual numerical decimal of accuracy.
                detection_frame = current_frame

                detection_result_list.clear()

            # if the detection frame has a box
            if detection_frame is not None:
                cv2.imshow('object_detection', detection_frame)
            Score = 0
            #print(Score)
            # Stop the program if the ESC key is pressed.
            if cv2.waitKey(1) == 27:
                break
                
        detector.close()
        capture.release()
        cv2.destroyAllWindows()


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--model',
        help='/Users/nabilmouss/Desktop/MODEL_PHONE/model.tflite',
        required=False,
        default='/Users/nabilmouss/Downloads/efficientdet_lite0.tflite')
    parser.add_argument(
        '--maxResults',
        help='1',
        required=False,
        default=10)
    parser.add_argument(
        '--scoreThreshold',
        help='0.90',
        required=False,
        type=float,
        default=0.40)
    # Finding the camera ID can be very reliant on platform-dependent methods. 
    # One common approach is to use the fact that camera IDs are usually indexed sequentially by the OS, starting from 0. 
    # Here, we use OpenCV and create a VideoCapture object for each potential ID with 'cap = cv2.VideoCapture(i)'.
    # If 'cap' is None or not 'cap.isOpened()', it indicates the camera ID is not available.
    parser.add_argument(
        '--cameraId', help='Id of camera.', required=False, type=int, default=0)
    parser.add_argument(
        '--frameWidth',
        help='256',
        required=False,
        type=int,
        default=1280)
    parser.add_argument(
        '--frameHeight',
        help='256',
        required=False,
        type=int,
        default=720)
    parser.add_argument(
        '--categoryAllowlist',
        help='Comma-separated list of allowed category names for detection.',
        required=False,
        default='truck,car,motorcycle,bus') # this is what the model detects nothing else
    args = parser.parse_args()

    category_allowlist = args.categoryAllowlist.split(',')
    run(args.model, int(args.maxResults),
        args.scoreThreshold, int(args.cameraId), args.frameWidth, args.frameHeight, category_allowlist)


if __name__ == '__main__':
    main()
