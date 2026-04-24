#!/usr/bin/env python3

import os
import yaml
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import JointState
from ament_index_python.packages import get_package_share_directory
from math import sin, cos, pi

class PosePublisher(Node):
    def __init__(self):
        super().__init__('pose_publisher_node')
        qos_profile = QoSProfile(depth=10)

        self.q1 = 0.0
        self.q2 = 0.0
        self.q3 = 0.0
        self.q4 = 0.0
        self.q5 = 0.0

        package_name = 'lab3'
        package_share_directory = get_package_share_directory(package_name)
        yaml_file_path = os.path.join(package_share_directory, 'config', 'lab3_config.yaml')

        with open(yaml_file_path, 'r') as file:
            params = yaml.safe_load(file)

        self.h = params['base_height'] + params['rotating_link_height']
        self.l1 = params['rear_arm_length']
        self.l2 = params['forearm_length']
        self.l3 = params['tool_length']

        self.pose_pub = self.create_publisher(PoseStamped, 'calculated_position', qos_profile)
        self.joint_sub = self.create_subscription(JointState, '/joint_states', self.joint_state_callback, 10)

    def joint_state_callback(self, msg):
        joints = dict(zip(msg.name, msg.position))
        self.q1 = joints.get('joint1', self.q1)
        self.q2 = joints.get('joint2', self.q2)
        self.q3 = joints.get('joint3', self.q3)
        self.q4 = joints.get('joint4', self.q4)
        self.q5 = joints.get('joint5', self.q5)

        pose_msg = PoseStamped()
        pose_msg.header.frame_id = 'base_link'
        pose_msg.header.stamp = self.get_clock().now().to_msg()

        total_pitch2 = self.q2
        total_pitch3 = self.q2 + self.q3
        total_pitch4 = self.q2 + self.q3 + self.q4

        r = self.l1 * sin(total_pitch2) + self.l2 * sin(total_pitch3) + self.l3 * sin(total_pitch4)
        z = self.h + self.l1 * cos(total_pitch2) + self.l2 * cos(total_pitch3) + self.l3 * cos(total_pitch4)

        x = r * cos(self.q1)
        y = r * sin(self.q1)

        pose_msg.pose.position.x = float(x)
        pose_msg.pose.position.y = float(y)
        pose_msg.pose.position.z = float(z)

        corrected_pitch = total_pitch4 - (pi / 2)

        qx, qy, qz, qw = self.euler_to_quaternion(self.q5, corrected_pitch, self.q1)

        pose_msg.pose.orientation.x = qx
        pose_msg.pose.orientation.y = qy
        pose_msg.pose.orientation.z = qz
        pose_msg.pose.orientation.w = qw

        self.pose_pub.publish(pose_msg)

    @staticmethod
    def euler_to_quaternion(r, p, y):
        qx = float(sin(r/2) * cos(p/2) * cos(y/2) - cos(r/2) * sin(p/2) * sin(y/2))
        qy = float(cos(r/2) * sin(p/2) * cos(y/2) + sin(r/2) * cos(p/2) * sin(y/2))
        qz = float(cos(r/2) * cos(p/2) * sin(y/2) - sin(r/2) * sin(p/2) * cos(y/2))
        qw = float(cos(r/2) * cos(p/2) * cos(y/2) + sin(r/2) * sin(p/2) * sin(y/2))
        return (qx, qy, qz, qw)

def main(args=None):
    rclpy.init(args=args)
    node = PosePublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()