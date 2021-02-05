#!/bin/bash

xfce4-terminal \
--tab --title "INIT" --command "bash -c \"  
cd /ws && source /opt/ros/foxy/setup.bash && colcon build && source ./install/setup.bash;
exec bash\""  \
--tab --title "FAKE CAMERA" --command "bash -c \"
sleep 5 && cd /ws && source ./install/setup.bash && ros2 launch template_pkg template_pkg.launch.py;
exec bash\""  \
--tab --title "IMAGE VIEWER"	--command "bash -c \"
sleep 10 && cd /ws && source ./install/setup.bash && ros2 run image_view image_view image:=/license_plate_detector/image_license_plate;
exec bash\""  \
--tab --title "LICENSE PLATE DETECTOR"	--command "bash -c \"
sleep 5 && cd /ws && source ./install/setup.bash && ros2 launch license_plate_detector license_plate_detector.launch.py;
exec bash\"" \
--tab --title "LICENSE PLATE SERVICE"	--command "bash -c \"
sleep 8 && cd /ws && source ./install/setup.bash && ros2 service call /license_plate_detector/start std_srvs/srv/Empty;
exec bash\"" & 