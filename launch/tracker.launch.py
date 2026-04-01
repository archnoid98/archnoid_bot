from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='archnoid_bot',
            executable='object_detector.py',  # Add .py here
            name='detector',
            output='screen'
        ),
        Node(
            package='archnoid_bot',
            executable='object_follower.py',  # Add .py here
            name='follower',
            output='screen'
        )
    ])