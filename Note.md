ROS2 setup



* [Ros2 Dashing full desktop installation Ubuntu 18.04](https://index.ros.org/doc/ros2/Installation/Dashing/Linux-Install-Debians/)

```
--Install
sudo apt update && sudo apt install curl gnupg2 lsb-release
curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -
sudo sh -c 'echo "deb [arch=$(dpkg --print-architecture)] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" > /etc/apt/sources.list.d/ros2-latest.list'
sudo apt update
sudo apt install ros-dashing-desktop
sudo apt install python3-colcon-common-extensions

# Extra add autocomplete
#sudo apt install -y python3-pip
```

--Remove
sudo apt remove ros-dashing-* && sudo apt autoremove
```


* [Create your first Ros2 package](https://index.ros.org/doc/ros2/Tutorials/Creating-Your-First-ROS2-Package/)

# # First build Setup virtualenv colcol python
source /opt/ros/dashing/setup.bash
cd ~/Documens/ws/
mkdir -p src
mkdir colcon-venv
python3 -m venv colcon-venv	
source colcon-venv/bin/activate
pip install argcomplete
pip install  colcon-common-extensions
pip install setuptools==40.0 pytest==5.0
colcon build
source install/setup.sh
```

```
# Package create
cd ~/Documens/ws/src	
ros2 pkg create --build-type ament_python --node-name license_plate_detector_node license_plate_detector
cd ~/Documens/ws/
colcon build
#colcon build --packages-select license_plate_detector 
source install/setup.bash
ros2 run license_plate_detector license_plate_detector_node
```

sudo apt install ros-dashing-v4l2-camera
sudo apt install ros-dashing-camera-info-manager
sudo apt install ros-dashing-vision-opencv 

ros2 pkg executables <pkg_name>


docker run --name ros2ws --network -it -v  /home/visionlab/Documents/ws/src:/ws/src  ros:foxy /bin/bash 
apt update
apt install python3-pip
pip3 install opencv-python



* [Publisher and subscriber Ros2](https://index.ros.org/doc/ros2/Tutorials/Writing-A-Simple-Py-Publisher-And-Subscriber/)

* (Colcon PDF doc](https://buildmedia.readthedocs.org/media/pdf/colcon/released/colcon.pdf)
