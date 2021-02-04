import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from rclpy.qos import qos_profile_sensor_data
import cv2
from cv_bridge import CvBridge, CvBridgeError
import numpy as np

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('template_pkg_subscriber_node')
        self.subscription = self.create_subscription( Image,'image_raw',self.listener_callback,10)
        self.subscription  # prevent unused variable warning
        self.value = 0
        self.publisher_ = self.create_publisher(Image, 'image_res', 10)
        timer_period = 0.5  # seconds
        self.i = 0
        self.bridge = CvBridge()

    def listener_callback(self, image):
        cv_image = self.bridge.imgmsg_to_cv2(image, desired_encoding='bgr8')

        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

        grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)

        abs_grad_x = cv2.convertScaleAbs(grad_x)
        abs_grad_y = cv2.convertScaleAbs(grad_y)

        grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
        outres = cv2.cvtColor(grad, cv2.COLOR_GRAY2BGR)
        self.publisher_.publish(self.bridge.cv2_to_imgmsg(np.array(outres), "bgr8"))
        #self.get_logger().info('Publishing an image')
        
def main(args=None):
    rclpy.init(args=args)
    minimal_subscriber = MinimalSubscriber()
    rclpy.spin(minimal_subscriber)
    print("Hello!")
    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()
    print("Goodbye!")

if __name__ == '__main__':
    main()
