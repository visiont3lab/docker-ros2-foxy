# ROS2 Foxy enviroment Docker setup

```
# First Time: Open  a terminal
echo "export ROS2_FOXY_ENV=$HOME/Documents/ws" >> $HOME/.bashrc && source $HOME/.bashrc
cd $ROS2_FOXY_ENV && ./scripts.sh

# Inside the docker
cd /home/ws/src  && ./installation.sh

# Second-Third - Time
docker start ros2ws
docker exec -it ros2ws /bin/bash
```