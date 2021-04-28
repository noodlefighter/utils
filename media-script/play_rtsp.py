import cv2
import time
from datetime import datetime
import getpass

# Use public RTSP Streaming for testing, but I am getting black frames!
cap = cv2.VideoCapture('rtsp://192.168.8.1:7070')
frameRate = cap.get(5) #frame rate
count = 0


while cap.isOpened():
    start_time = time.time()

    frameId = cap.get(1)  # current frame number
    ret, frame = cap.read()

    if (ret != True):
        break

    # Show frame for testing
    cv2.imshow('frame', frame)
    cv2.waitKey(1)

    count += 1

    #Break loop after 5*60 minus
    if count > 5*60:
        break

    elapsed_time = time.time() - start_time

    # Wait for 60 seconds (subtract elapsed_time in order to be accurate).
    time.sleep(60 - elapsed_time)


cap.release()
print ("Done!")

cv2.destroyAllWindows()
