#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Point
from cv_bridge import CvBridge
import cv2
import numpy as np

class ObjectDetector(Node):
    def __init__(self):
        super().__init__('object_detector')
        # Ensure this matches the topic from your esp32_cam_bridge
        self.subscription = self.create_subscription(
            Image, 
            '/image_raw', 
            self.image_callback, 
            10)
        self.publisher_ = self.create_publisher(Point, '/detected_object', 10)
        self.bridge = CvBridge()
        
        # HSV Range for Green (Tune these!)
        self.low_green = np.array([35, 50, 50])
        self.high_green = np.array([90, 255, 255])
        
        self.get_logger().info("Object Detector Node Started. Looking for green...")

    def image_callback(self, msg):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, self.low_green, self.high_green)
            
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if contours:
                largest_contour = max(contours, key=cv2.contourArea)
                if cv2.contourArea(largest_contour) > 500:
                    M = cv2.moments(largest_contour)
                    if M["m00"] != 0:
                        center_x = int(M["m10"] / M["m00"])
                        center_y = int(M["m01"] / M["m00"])
                        
                        width = cv_image.shape[1]
                        norm_x = (center_x - (width / 2)) / (width / 2)
                        norm_area = cv2.contourArea(largest_contour) / (cv_image.shape[0] * cv_image.shape[1])
                        
                        msg_point = Point()
                        msg_point.x = float(norm_x)
                        msg_point.y = float(center_y)
                        msg_point.z = float(norm_area) 
                        self.publisher_.publish(msg_point)
        except Exception as e:
            self.get_logger().error(f"Error in image_callback: {e}")

# --- CRITICAL SECTION: THE ENTRY POINT ---
def main(args=None):
    rclpy.init(args=args)
    node = ObjectDetector()
    try:
        rclpy.spin(node) # This keeps the node alive!
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down Object Detector...")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()