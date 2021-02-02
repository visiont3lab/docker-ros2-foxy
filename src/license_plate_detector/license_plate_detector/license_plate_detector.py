import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import cv2
import numpy as np

class LicensePlateDetector(Node):
    def __init__(self):
        super().__init__('license_plate_detector_node')
        self.image_sub = self.create_subscription( Image, '/v4l2_camera/image_raw', self.image_cb,10)
        self.image_sub  # prevent unused variable warning
        
        self.image_pub = self.create_publisher(Image, 'image_license_plate', 10)
        self.bridge = CvBridge()

    def image_cb(self, image):
        # Subscriber
        try:
            frame = self.bridge.imgmsg_to_cv2(image, desired_encoding='bgr8')
        
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            
            outres = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
            self.image_pub.publish(self.bridge.cv2_to_imgmsg(np.array(outres), "bgr8"))
        except:
            pass
        
def main(args=None):
    rclpy.init(args=args)
    MyLicensePlateDetector = LicensePlateDetector()
    rclpy.spin(MyLicensePlateDetector)
    # Destroy node
    MyLicensePlateDetector.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
   main()