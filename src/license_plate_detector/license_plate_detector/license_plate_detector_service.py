from custom_interfaces.srv import MyCustom

import rclpy
from rclpy.node import Node

# https://index.ros.org/doc/ros2/Tutorials/Writing-A-Simple-Py-Service-And-Client/

class LicensePlateDetectorService(Node):

    def __init__(self):
        super().__init__('license_plate_detector_service')
        self.srv = self.create_service(MyCustom, 'process_video', self.process_video_cb)

    def process_video_cb(self, request, response):
        
        response.message = "BABY"
        response.res = True
        
        print(response.res,response.message,request.path)

        return response


def main(args=None):
    rclpy.init(args=args)

    MyLicensePlateDetectorService = LicensePlateDetectorService()

    rclpy.spin(MyLicensePlateDetectorService)

    rclpy.shutdown()


if __name__ == '__main__':
    main()