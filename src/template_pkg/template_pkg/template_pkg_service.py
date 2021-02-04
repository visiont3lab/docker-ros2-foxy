from custom_interfaces.srv import SetBool

'''
SetBool
bool data # e.g. for hardware enabling / disabling
---
bool success   # indicate successful run of triggered service
string message # informational, e.g. for error messages

'''

import rclpy
from rclpy.node import Node

# https://index.ros.org/doc/ros2/Tutorials/Writing-A-Simple-Py-Service-And-Client/

class LicensePlateDetectorService(Node):

    def __init__(self):
        super().__init__('template_pkg_service_node')
        self.srv = self.create_service(SetBool, 'test', self.my_cb)

    def my_cb(self, request, response):
        
        response.message = "BABY"
        response.success = True
        
        print(response.res,response.message,request.data)

        return response


def main(args=None):
    rclpy.init(args=args)

    MyLicensePlateDetectorService = LicensePlateDetectorService()

    rclpy.spin(MyLicensePlateDetectorService)

    rclpy.shutdown()


if __name__ == '__main__':
    main()