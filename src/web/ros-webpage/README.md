# Ros web page to control a robot

Create indext.html

```
# we need python3
cd thermal_ws
source myenv/bin/activate
pip install httpserver
cd ros-webpage
python -m http.server --bind 0.0.0.0  8900
```

```
# bridge server

cd thermal_ws
source myenv/bin/activate
pip install twisted pyOpenSSL  autobahn tornado  service_identity pymongo  Pillow
catkin_make
roslaunch rosbridge_server rosbridge_websocket.launch 

```