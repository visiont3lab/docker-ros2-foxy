import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from cv_bridge import CvBridge
from sensor_msgs.msg import Image,CompressedImage
import cv2
import numpy as np
import os 
import sys
from ament_index_python.packages import get_package_share_directory
import cv2

class MinimalPublisherNode(Node):
      def __init__(self):
         super().__init__('template_pkg_publisher_node')

         self.full_path = os.path.join(get_package_share_directory('template_pkg'), 'images')
         self.paths = os.listdir(self.full_path) 

         self.publisher_ = self.create_publisher(CompressedImage, 'image_raw/compressed', 10)
         timer_period = 0.5  # seconds
         #self.timer = self.create_timer(timer_period, self.timer_callback)
         self.bridge = CvBridge()
         self.i=0

         self.publish_video()

      def publish_video(self):
         # Video
         cap = cv2.VideoCapture(os.path.join(get_package_share_directory('template_pkg'), 'videos', 'piazzaDiSpagna.mp4'))
         while(cap.isOpened()):
            ret, frame = cap.read()
            if ret==True: 			
               imgmsg = self.bridge.cv2_to_compressed_imgmsg(frame,dst_format='jpg')
               self.publisher_.publish(imgmsg) #self.bridge.cv2_to_imgmsg(np.array(frame), "bgr8"))
            cv2.waitKey(1)      

         cap.release()
         cv2.destroyAllWindows()

      def timer_callback(self):
         name = os.path.join(self.full_path,self.paths[self.i])
         im = cv2.imread(name, 1)
         self.publisher_.publish(self.bridge.cv2_to_imgmsg(np.array(im), "bgr8"))
         self.i = self.i+1
         #self.get_logger().info('Publishing an image')
         if self.i==((len(self.paths)-1)):
            self.i=0

def main(args=None):
    rclpy.init(args=args)
    MyMinimalPublisherNode = MinimalPublisherNode()
    rclpy.spin(MyMinimalPublisherNode)
    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
   main()