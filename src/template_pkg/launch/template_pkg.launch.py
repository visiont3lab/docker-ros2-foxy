from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='template_pkg',
            namespace='template_pkg',
            executable='template_pkg_publisher_node',
            name='template_pkg_publisher_node',
            output='screen'
        ),
    ])