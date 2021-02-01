apt update && apt install inetutils-ping python3-pip ros-foxy-vision-opencv -y
apt install libgl1-mesa-glx -y
pip3 install opencv-python
colcon build && source ./install/setup.bash && export ROS_DOMAIN_ID=13 && source ./install/setup.bash 
# ROS_DOMAIN_ID=13 ros2 topic list
# ros2 run mypkg listener
# sudo ufw disable