import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import cv2
import numpy as np

class MinimalPublisher(Node):
      def __init__(self):
         super().__init__('minimal_publisher')
         self.publisher_ = self.create_publisher(Image, 'image_raw', 10)
         timer_period = 0.5  # seconds
         self.timer = self.create_timer(timer_period, self.timer_callback)
         self.i = 0
         self.im_list = []
         self.cv_image = cv2.imread('/home/andrea/Desktop/9kquktfl42r41.jpg') ### an RGB image 
         self.bridge = CvBridge()

      def timer_callback(self):
         self.publisher_.publish(self.bridge.cv2_to_imgmsg(np.array(self.cv_image), "bgr8"))
         self.get_logger().info('Publishing an image')

def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
   main()