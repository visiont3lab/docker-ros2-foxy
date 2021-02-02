from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='license_plate_detector',
            namespace='license_plate_detector',
            executable='license_plate_detector_node',
            name='license_plate_detector_node',
            output='screen'
        ),
    ])