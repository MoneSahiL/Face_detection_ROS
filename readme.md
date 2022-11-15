This package is built for detecting person in frame.
MobileNetSSD is used for the detection.

Keep the package in '/catkin_ws/src'
'catkin_make' the package in catkin_ws deirectory

Run  - 'roslaunch human_detection human_detection_launch.launch'
	or 'rosrun human_detection my_human_detection.py'
	
	
In second terminal, run - 'rosbag record --duration=60 -O human_detection.bag /webcam' to record the webcam topic for 60 seconds and create a bag.


press ctrl+c in running terminal to exit.



rosbag info -

seikh@ub20:~/catkin_ws$ rosbag info src/human_detection/rosbag/human_detection.bag 
path:        src/human_detection/rosbag/human_detection.bag
version:     2.0
duration:    59.7s
start:       Oct 29 2022 16:18:47.65 (1667053127.65)
end:         Oct 29 2022 16:19:47.35 (1667053187.35)
size:        1.5 GB
messages:    599
compression: none [599/599 chunks]
types:       sensor_msgs/Image [060021388200f6f0f447d0fcd9c64743]
topics:      /webcam   599 msgs    : sensor_msgs/Image


