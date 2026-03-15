import os
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='esp32_cam_bridge',
            executable='cam_node',
            output='screen',
            parameters=[{
                'esp32_ip': '192.168.68.110'
            }]
        )
    ])