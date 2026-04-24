import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    package_name = 'lab4'

    rviz_config_path = os.path.join(
        get_package_share_directory(package_name),
        'rviz',
        'lab4.rviz'
    )

    urdf_file = os.path.join(
        get_package_share_directory(package_name),
        'urdf',
        'lab4.urdf.xacro'
    )

    doc = xacro.process_file(urdf_file)
    robot_description = {'robot_description': doc.toxml()}

    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[robot_description]
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config_path],
            output='screen'
        ),
        Node(
            package=package_name,
            executable='DobotMover.py',
            name='MoveToPoint'
        ),
        Node(
            package=package_name,
            executable='DobotKin.py',
            name='JointStatesConverter'
        ),
    ])