import cv2  
import math
import serial
import time
from cvzone.HandTrackingModule import HandDetector

# Set up serial communication
arduino_port = 'COM5'  # Change this to your Arduino port
baud_rate = 9600
arduino = serial.Serial(arduino_port, baud_rate, timeout=1)
time.sleep(2)  # Give some time for the serial connection to establish

# Initialize the camera
cap = cv2.VideoCapture(0)

# Set up the hand tracking object
detector = HandDetector(detectionCon=0.8)

# Start the while loop
while True:
    success, image = cap.read()
    hands, bboxInfo = detector.findHands(image)

    if len(hands) > 0:
        # Find the largest hand based on bounding box area
        bboxInfo=hands[0]['bbox']
        largest_hand_index = 0
        largest_area = bboxInfo[2] * bboxInfo[3]

        for i in range(1, len(hands)):
            bboxInfo=hands[i]['bbox']
            area = bboxInfo[2] * bboxInfo[3]
            if area > largest_area:
                largest_area = area
                largest_hand_index = i

        # Calculate the angle for the largest hand
        hand = hands[largest_hand_index]
        h = hand['lmList'][8][0] - hand['lmList'][6][0]  # x-coordinates of index and middle finger tips
        b = hand['lmList'][6][1] - hand['lmList'][8][1]  # y-coordinates of index and middle finger tips

        if b == 0:
            b += 0.000001
            angle = math.degrees(math.atan(h / b))
        else:
            if h < 0 and b < 0:
                angle = -90
            elif h > 0 and b < 0:
                angle = 90
            else:
                angle = math.degrees(math.atan(h / b))

        print(angle)
        arduino_data = f"{angle}\n"
        arduino.write(arduino_data.encode('utf-8'))

    cv2.imshow('image', image)      
    cv2.waitKey(1)   

arduino.close()
