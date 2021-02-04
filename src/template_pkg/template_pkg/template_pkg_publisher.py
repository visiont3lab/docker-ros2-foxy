import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import cv2
import numpy as np
import os 

class MinimalPublisher(Node):
      def __init__(self):
         super().__init__('template_pkg_publisher_node')
         self.publisher_ = self.create_publisher(Image, 'image_raw', 10)
         timer_period = 0.5  # seconds
         self.timer = self.create_timer(timer_period, self.timer_callback)
         path = os.path.join('/ws/src/template_pkg/template_pkg','data','sample1.png')
         self.cv_image = cv2.imread(path,1) ### an RGB image 
         self.bridge = CvBridge()

      def timer_callback(self):
         self.publisher_.publish(self.bridge.cv2_to_imgmsg(np.array(self.cv_image), "bgr8"))
         #self.get_logger().info('Publishing an image')

def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
   main()