from custom_interfaces.srv import MyCustom
import rclpy
from rclpy.node import Node
from ament_index_python.packages import get_package_share_directory
from license_plate_detector.src.utilsLicensePlate import LicensePlateDetector    
import os
import cv2 
from datetime import datetime 

'''
# https://index.ros.org/doc/ros2/Tutorials/Writing-A-Simple-Py-Service-And-Client/

string path
string cmd
---
bool res
string message

#  ros2 service call /process_video custom_interfaces/srv/MyCustom "{path: "/ws/src/license_plate_detector/license_plate_detector/src/datasets/video/parking10.mp4", cmd: "start"}"
#  ros2 service call /process_video custom_interfaces/srv/MyCustom "{path: "/ws/src/license_plate_detector/license_plate_detector/src/datasets/video/parking5.mp4", cmd: "start"}"
'''

class LicensePlateDetectorService(Node):

    def __init__(self):
        super().__init__('license_plate_detector_service')
        
        self.srv_pv_start = self.create_service(MyCustom, 'process_video', self.pv_cb)
        model_path = os.path.join(get_package_share_directory('license_plate_detector'), 'data', 'lp-detector','wpod-net_update1.h5')
        self.Lpd = LicensePlateDetector(model_path)
 
    def pv_cb(self, request, response):
        print("START")
        now = datetime.now()
        name = now.strftime("%m_%d_%Y_%H_%M_%S")
        #inp_path = "/ws/src/license_plate_detector/license_plate_detector/src/datasets/video/parking10.mp4"
        out_path = "/ws/src/license_plate_detector/license_plate_detector/src/datasets/video/"+name+"_video.mp4"
     
        self.Lpd.processVideo(request.path,out_path)

        response.message = out_path
        response.res = True
        
        return response

def main(args=None):
    rclpy.init(args=args)

    MyLicensePlateDetectorService = LicensePlateDetectorService()

    rclpy.spin(MyLicensePlateDetectorService)

    rclpy.shutdown()


if __name__ == '__main__':
    main()