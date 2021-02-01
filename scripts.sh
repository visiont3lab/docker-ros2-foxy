#!/bin/bash
xhost +local:docker && \
docker run -it \
    --name ros2ws \
    --network host \
    --pid host  \
    --env="DISPLAY=$DISPLAY" \
    --env="QT_X11_NO_MITSHM=1" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    -v /home/visionlab/Documents/ws/src:/ws/src \
    ros:foxy \
    bash 

# Extra: https://github.com/visiont3lab/docker-ros-laser-sim/blob/master/scripts/start_docker_laser_sim.sh
# apt update && apt install inetutils-ping python3-pip  -y
# apt install libgl1-mesa-glx
# apt instal vision-opencv
# pip3 install opencv-python
# cd ws && colcon build && source ./install/setup.bash && export ROS_DOMAIN_ID=13 && source ./install/setup.bash 
# ROS_DOMAIN_ID=13 ros2 topic list
# ros2 run mypkg listener
# sudo ufw disable
# ros2 pkg executables <package-name>