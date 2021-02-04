import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import cv2
import numpy as np
import os 
import sys
from ament_index_python.packages import get_package_share_directory

class MinimalPublisher(Node):
      def __init__(self):
         super().__init__('template_pkg_publisher_node')

         self.full_path = os.path.join(get_package_share_directory('template_pkg'), 'images')
         self.paths = os.listdir(self.full_path) 

         self.publisher_ = self.create_publisher(Image, 'image_raw', 10)
         timer_period = 0.5  # seconds
         self.timer = self.create_timer(timer_period, self.timer_callback)
         self.bridge = CvBridge()

      def timer_callback(self):
         for i in range(0,len(self.paths)):
            name = os.path.join(self.full_path,self.paths[i])
            im = cv2.imread(name, 1)
            self.publisher_.publish(self.bridge.cv2_to_imgmsg(np.array(im), "bgr8"))
            #self.get_logger().info('Publishing an image')
            if i==((len(self.paths)-1)):
               i=0

def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
   main()