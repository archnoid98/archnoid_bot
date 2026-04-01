#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point, Twist

class ObjectFollower(Node):
    def __init__(self):
        super().__init__('object_follower')
        
        # Subscribe to the coordinates from the detector
        self.subscription = self.create_subscription(
            Point,
            '/detected_object',
            self.listener_callback,
            10)
        
        # Publish to the tracker topic (configured in your twist_mux)
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel_tracker', 10)
        
        # --- GAIN TUNING ---
        # Adjust these if the robot is too slow or too twitchy
        self.angular_gain = -1.2  # Turn speed
        self.linear_gain = 0.6    # Forward speed
        self.target_area = 0.08   # The 'stop' distance (8% of frame)
        self.area_threshold = 0.005 # Minimum area to even bother moving
        
        self.get_logger().info("Object Follower Node Started. Waiting for green T-shirt...")

    def listener_callback(self, msg):
        twist = Twist()
        
        # 1. Check if the object is large enough to be 'real'
        if msg.z > self.area_threshold:
            # 2. Rotation Logic (P-Control)
            # msg.x is -1.0 (left) to 1.0 (right). 
            # If x is 0.5, we need negative angular.z to turn right.
            twist.angular.z = msg.x * self.angular_gain
            
            # 3. Translation Logic (Forward/Backward)
            # area_error = target - current. 
            # Positive error means we are too far -> move forward.
            area_error = self.target_area - msg.z
            
            if area_error > 0.02: # Deadzone to prevent jittering when close
                twist.linear.x = area_error * self.linear_gain
            else:
                twist.linear.x = 0.0
                
            # Log for debugging
            # self.get_logger().info(f"X: {msg.x:.2f} | Area: {msg.z:.3f} | Lin: {twist.linear.x:.2f}")
        else:
            # If object is lost, stop moving
            twist.linear.x = 0.0
            twist.angular.z = 0.0
            
        self.publisher_.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = ObjectFollower()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down Object Follower...")
    finally:
        # Stop the robot on exit
        stop_msg = Twist()
        node.publisher_.publish(stop_msg)
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()