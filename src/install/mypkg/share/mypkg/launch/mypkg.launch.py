from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='mypkg',
            node_namespace='minimal_publisher1',
            node_executable='listener',
            node_name='mypkg_subscriber'
        ),
    ])