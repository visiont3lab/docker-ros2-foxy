# ROS2 Foxy enviroment Docker setup

```
# First Time: Open  a terminal
sudo apt install xfce4-terminal
echo "export ROS2_FOXY_ENV=$HOME/Documents/ws" >> $HOME/.bashrc && source $HOME/.bashrc
cd $ROS2_FOXY_ENV/src/launchers && ./start_ros_foxy_ws.sh

# Inside the docker
cd /ws/src/lauchers  && ./launch_real_time_license_plate_detector.sh

# Extra - Build custom docker image
cd $ROS2_FOXY_ENV &&  docker build -t ros2ws:custom  --network host .
docker start ros2ws 
docker exec -it ros2ws /bin/bash
#docker tag ros2ws:custom visiont3lab/ros2ws:custom
docker tag ros2ws:custom visiont3lab/ros2ws:web
```



