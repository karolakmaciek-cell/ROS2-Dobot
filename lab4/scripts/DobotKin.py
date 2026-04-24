#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from sensor_msgs.msg import JointState
import math

class DobotPublisher(Node):
    def __init__(self):
        super().__init__('dobot_pose_publisher_node')
        qos_profile = QoSProfile(depth=10)

        self.q1 = 0.0
        self.q2 = 0.0
        self.q3 = 0.0
        self.q4 = 0.0
        self.q5 = 0.0
        
        #Subskrybent topic /dobot_joint_states
        self.joint_sub = self.create_subscription(JointState, '/dobot_joint_states', self.joint_state_callback, 10)
        self.pose_pub = self.create_publisher(JointState, '/joint_states', qos_profile)

    def joint_state_callback(self, msg):
        if (len(msg.position) < 4):
            return
        
        try:
            q1 = msg.position[0]
            q2 = msg.position[1]
            q3 = msg.position[2] + math.pi/2 - q2
            q5 = msg.position[3]

        except IndexError:
            
            return

        q4 = -(q2 + q3) + math.pi

        new_message = JointState()
        new_message.header = msg.header
        new_message.header.stamp = self.get_clock().now().to_msg()
        new_message.name = ['joint1', 'joint2', 'joint3', 'joint4', 'joint5']
        new_message.position = [q1, q2, q3, q4, q5]
        self.pose_pub.publish(new_message)

def main(args=None):
    rclpy.init(args=args)
    node = DobotPublisher()
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