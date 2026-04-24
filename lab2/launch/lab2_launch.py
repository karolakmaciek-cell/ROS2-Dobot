from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            'tower_height',
            default_value='3',
            description='Wysokosc wiezy do zbudowania przez robota'
        ),

        Node(
            package='lab2',
            executable='tower_maker',
            name='dobot_tower_maker',
            output='screen',
            parameters=[{
                'tower_height': LaunchConfiguration('tower_height'),
            }]
        )
    ])