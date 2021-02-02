#!/bin/bash

xfce4-terminal \
--tab --title "INIT" --command "bash -c \"  
sleep 4 && cd /ws && source /opt/ros/foxy/setup.bash && colcon build && source ./install/setup.bash;
exec bash\""  \
--tab --title "USB CAMERA" --command "bash -c \"
sleep 10 && cd /ws && source ./install/setup.bash && ros2 launch src/v4l2_camera/launch/vl4l2_camera.launch.py;
exec bash\""  \
--tab --title "IMAGE VIEWER"	--command "bash -c \"
sleep 10 && cd /ws && source ./install/setup.bash && ros2 run rqt_image_view rqt_image_view;
exec bash\""  \
--tab --title "LICENSE PLATE DETECTOR"	--command "bash -c \"
sleep 10 && cd /ws && source ./install/setup.bash && ros2 launch license_plate_detector license_plate_detector.launch.py;
exec bash\"" & 