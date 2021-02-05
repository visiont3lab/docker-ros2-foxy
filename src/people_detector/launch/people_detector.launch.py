from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='people_detector',
            namespace='people_detector',
            executable='people_detector_node',
            name='people_detector_node',
            output='screen'
        ),
    ])
