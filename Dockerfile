FROM ros:foxy

# General dependencies
RUN apt-get update && apt-get install -y inetutils-ping git vim wget htop unzip net-tools cmake

# Extra
RUN apt-get update && apt-get install -y python3-pip ros-foxy-vision-opencv ros-foxy-image-transport ros-foxy-camera-info-manager ros-foxy-rqt-image-view

# X11 forwarding dependencies
RUN apt-get update && apt-get install -y libgl1-mesa-dev ffmpeg libsm6 libxext6 libxrender-dev libgtk2.0-dev 

# License Plate Python Dependencies
RUN pip3 install h5py==2.10.0 numpy==1.19.5 Keras==2.4.3 opencv-python==4.5.1.48 tensorflow==2.4.1

# Xfce terminal
RUN apt-get update && apt-get install -y xfce4-terminal

# Important use --network host otherwise image cannot access network
# docker build -t ros2ws:custom  --network host .
