from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='template_pkg',
            node_namespace='minimal_publisher1',
            node_executable='listener_node',
            node_name='template_pkg_subscriber',
            output='screen'
        ),
    ])