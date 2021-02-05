#!/bin/bash

xfce4-terminal \
--tab --title "INIT" --command "bash -c \"  
cd /ws && source /opt/ros/foxy/setup.bash && colcon build && source ./install/setup.bash;
exec bash\""  \
--tab --title "FAKE CAMERA" --command "bash -c \"
sleep 5 && cd /ws && source ./install/setup.bash && ros2 launch template_pkg template_pkg.launch.py;
exec bash\""  \
--tab --title "PEOPLE DETECTOR"	--command "bash -c \"
sleep 5 && cd /ws && source ./install/setup.bash && ros2 launch people_detector people_detector.launch.py;
exec bash\"" \
--tab --title "PEOPLE DETECTOR SERVICE"	--command "bash -c \"
sleep 8 && cd /ws && source ./install/setup.bash && ros2 service call /people_detector/start std_srvs/srv/Empty;
exec bash\"" & 