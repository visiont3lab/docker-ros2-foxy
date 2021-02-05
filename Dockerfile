FROM ros:foxy

# General dependencies
RUN apt-get update && apt-get install -y inetutils-ping git vim wget htop unzip net-tools cmake curl

# Extra
RUN apt-get update && apt-get install -y python3-pip ros-foxy-vision-opencv ros-foxy-image-transport ros-foxy-camera-info-manager ros-foxy-rqt-image-view

# X11 forwarding dependencies
RUN apt-get update && apt-get install -y libgl1-mesa-dev ffmpeg libsm6 libxext6 libxrender-dev libgtk2.0-dev 

# License Plate Python Dependencies
RUN pip3 install h5py==2.10.0 numpy==1.19.5 Keras==2.4.3 opencv-python==4.2.0.34 tensorflow==2.4.1 imutils

# Xfce terminal
RUN apt-get update && apt-get install -y xfce4-terminal nodejs npm 

# Setup nodejs 14 
RUN curl -sL https://deb.nodesource.com/setup_14.x | sudo -E bash - && apt-get install -y nodejs

# Setup ros user
# RUN useradd  -p ros -ms /bin/bash  ros
# USER ros
WORKDIR  /ws/src

# Important use --network host otherwise image cannot access network
# docker build -t ros2ws:custom  --network host .
# remember to build cd src/web/ros2-web-bridge npm install && npm rebuild
# apt install ros-foxy-image-transport-plugins