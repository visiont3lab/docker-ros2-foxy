#!/bin/bash
#!/bin/bash

xhost +local:docker && \
docker run -it --rm \
    --name ros2ws \
    --network host \
    --pid host  \
    --env="DISPLAY=$DISPLAY" \
    --env="QT_X11_NO_MITSHM=1" \
    --device=/dev/video0 \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    -v $ROS2_FOXY_ENV/src:/ws/src \
    visiont3lab/ros2ws:custom \
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

# v4l2-ctl -d /dev/video0 -c exposure_auto=1 
# v4l2-ctl -d /dev/video0 -c white_balance_temperature_auto=0
