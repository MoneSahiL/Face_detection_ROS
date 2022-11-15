#!/usr/bin/python3

import rospy
from sensor_msgs.msg import Image
import numpy as np
import cv2
from cv_bridge import CvBridge
from pathlib import Path
HOME = str(Path.home())

protxt = HOME + "/catkin_ws/src/human_detection/include/MobileNetSSD_deploy.prototxt.txt"
model = HOME + "/catkin_ws/src/human_detection/include/MobileNetSSD_deploy.caffemodel"
conf = 0.2

CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]

COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

net = cv2.dnn.readNetFromCaffe(protxt, model)

pub = rospy.Publisher('webcam', Image, queue_size=10)
rospy.init_node('team_vibot_camera', anonymous=True)
rate = rospy.Rate(10) # 10hz
bridge = CvBridge()
cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture("images/example_14.jpg")
# cap = cv2.imread("images/example_14.jpg")

# while True:
while not rospy.is_shutdown():
    ret, frame = cap.read()
    frame_resized = cv2.resize(frame,(300,300))
    (h, w) = frame.shape[:2]

    blob = cv2.dnn.blobFromImage(frame_resized, 0.007843, (300, 300), (127.5, 127.5, 127.5), False)

    net.setInput(blob)

    detections = net.forward()

    for i in np.arange(0, detections.shape[2]):
        
        confidence = detections[0, 0, i, 2]

        if confidence > conf:
            idx = int(detections[0, 0, i, 1])
#            print(idx)

            if idx == 15:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
                print("[INFO] {}".format(label))
                cv2.rectangle(frame, (startX, startY), (endX, endY),
                    COLORS[idx], 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(frame, label, (startX, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
            ros_image = bridge.cv2_to_imgmsg(frame, encoding="bgr8") 
            pub.publish(ros_image)
            cv2.imshow("Output", frame)

            if cv2.waitKey(1) >= 0:
                break
