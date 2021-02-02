#!/bin/bash

# Ros utils
#apt update && apt install inetutils-ping python3-pip ros-foxy-vision-opencv ros-foxy-image-transport ros-foxy-camera-info-manager ros-foxy-rqt-image-view -y

# Grafics libgl
#apt install libgl1-mesa-glx -y

# License plate detector python requirements
#pip3 install opencv-python
#./src/license_plate_detector/license_plate_detector/install.sh

# Ros2 build
#cd .. && colcon build && source ./install/setup.bash && export ROS_DOMAIN_ID=13 && source ./install/setup.bash 
cd .. && colcon build && source ./install/setup.bash 

# ROS_DOMAIN_ID=13 ros2 topic list
# ros2 run mypkg listener
# sudo ufw disable