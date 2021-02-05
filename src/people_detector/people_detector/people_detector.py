import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from cv_bridge import CvBridge
from sensor_msgs.msg import Image,CompressedImage
import cv2
import numpy as np
from std_srvs.srv import Empty
from ament_index_python.packages import get_package_share_directory
from people_detector.src.utilsPeopleDetector import PeopleDetector    
import os

class PeopleDetectorNode(Node):
    def __init__(self):
        super().__init__('people_detector_node')
        #self.image_sub = self.create_subscription( Image, '/v4l2_camera/image_raw', self.image_cb,10)
        self.image_sub = self.create_subscription( CompressedImage, '/template_pkg/image_raw/compressed', self.image_cb,100)
        self.image_pub = self.create_publisher(Image, 'image/yolo', 10)
        self.srv_start = self.create_service(Empty, 'start', self.start_cb)
        self.srv_stop = self.create_service(Empty, 'stop', self.stop_cb)
        self.bridge = CvBridge()
        self.processing = False
        model_path = os.path.join(get_package_share_directory('people_detector'),  'models', 'yolo')
        self.peopleDetector = PeopleDetector(model_path)
        
    def image_cb(self, msg):
        # Subscriber
        #try:
        cv2.namedWindow("Results", cv2.WINDOW_NORMAL)
        if (self.processing==True):
            #frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            frame = self.bridge.compressed_imgmsg_to_cv2(msg) # desired_encoding='bgr8')
            
            #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            #outres = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
            
            res,imDraw,coordinates = self.peopleDetector.processImageSplit(frame)
            if res:
                frame = imDraw
            
            cv2.imshow("Results", frame)
            cv2.waitKey(1)
            #self.image_pub.publish(self.bridge.cv2_to_imgmsg(np.array(frame), "bgr8"))
        #except:
        #    pass
        
    def start_cb(self, request, response):
        print("Start")
        self.processing = True
        return response
   
    def stop_cb(self, request, response):
        print("Stop")
        self.processing = False
        return response

def main(args=None):
    rclpy.init(args=args)
    MyPeopleDetectorNode = PeopleDetectorNode()
    rclpy.spin(MyPeopleDetectorNode)
    # Destroy node
    MyPeopleDetectorNode.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
   main()