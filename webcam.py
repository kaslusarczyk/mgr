import cv2
import datetime
import sys
import math

cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

video_file = sys.argv[1]
video_capture = cv2.VideoCapture(video_file)

video_timestamp_s = 25

# Get frame rate
fps = video_capture.get(cv2.cv.CV_CAP_PROP_FPS)
print("Frames per second: {0}".format(fps))

frame_start_position = math.floor(video_timestamp_s * fps)
print("Frame start position: {0}".format(frame_start_position))

frames_count = video_capture.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
print("Total frames count: {0}".format(frames_count))

# Set frame position
video_capture.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, frame_start_position)

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )

    print("Found {0} faces!".format(len(faces)))

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    # Get current position of the video file in milliseconds
    video_capture_timestamp = video_capture.get(cv2.cv.CV_CAP_PROP_POS_MSEC)
    print("Video capture timestamp (ms): {0}".format(video_capture_timestamp))

    # Save image
    if len(faces) > 0:
        cv2.imwrite("face_" + datetime.datetime.now().isoformat()+".png", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
