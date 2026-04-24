#!/usr/bin/env python3
import os
import yaml
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from geometry_msgs.msg import PointStamped
from sensor_msgs.msg import JointState
from dobot_msgs.action import PointToPoint
from rclpy.qos import QoSProfile
from ament_index_python.packages import get_package_share_directory
from math import sin, cos, acos, atan2, sqrt, pi


class DobotMover(Node):
    def __init__(self):
        super().__init__('dobot_mover')
        qos_profile = QoSProfile(depth=10)

        package_name = 'lab4'
        package_share_directory = get_package_share_directory(package_name)
        yaml_file_path = os.path.join(package_share_directory, 'config', 'lab4_config.yaml')

        with open(yaml_file_path, 'r') as file:
            params = yaml.safe_load(file)

        self.h = params['base_height'] + params.get('rotating_link_height', 0.0)
        self.l1 = params['rear_arm_length']
        self.l2 = params['forearm_length']
        self.l3 = params['tool_length']
        
        self.j1_min = params.get('j1_min')
        self.j1_max = params.get('j1_max')
        self.j2_min = params.get('j2_min')
        self.j2_max = params.get('j2_max')
        self.j3_min = params.get('j3_min')
        self.j3_max = params.get('j3_max')
        self.j4_min = params.get('j4_min')
        self.j4_max = params.get('j4_max')

        self.sub_clicked = self.create_subscription(PointStamped, '/clicked_point', self.clicked_point_callback, qos_profile)
        self._action_client = ActionClient(self, PointToPoint, '/PTP_action')

        self.declare_parameter('phi_deg', 0.0)
        self.declare_parameter('motion_type', 1)
        self.declare_parameter('velocity_ratio', 0.5)
        self.declare_parameter('acceleration_ratio', 0.5)
        self.declare_parameter('tooltip_offset', 100.0)


    def clicked_point_callback(self, msg):
        x = msg.point.x
        y = msg.point.y
        z = msg.point.z

        x_mm = x * 1000.0
        y_mm = y * 1000.0
        z_mm = z * 1000.0

        phi = self.get_parameter('phi_deg').get_parameter_value().double_value
        m_type = self.get_parameter('motion_type').get_parameter_value().integer_value
        v_ratio = self.get_parameter('velocity_ratio').get_parameter_value().double_value
        a_ratio = self.get_parameter('acceleration_ratio').get_parameter_value().double_value
        t_offset = self.get_parameter('tooltip_offset').get_parameter_value().double_value

        self.get_logger().info(f"X={x_mm:.1f}, Y={y_mm:.1f}, Z={(z_mm - t_offset):.1f}")

        goal_msg = PointToPoint.Goal()
        goal_msg.motion_type = m_type
        goal_msg.target_pose = [float(x_mm), float(y_mm), float(z_mm - t_offset - 20), float(phi)]
        goal_msg.velocity_ratio = float(v_ratio)
        goal_msg.acceleration_ratio = float(a_ratio)
        
        if not self._action_client.wait_for_server(timeout_sec=2.0):
            return
        
        self._send_goal_future = self._action_client.send_goal_async(goal_msg, feedback_callback=self.feedback_callback)
        self._send_goal_future.add_done_callback(self.goal_response_callback)
        
    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().warning('Cel odrzucony')
            return

        self.get_logger().info('Cel zaakceptowany')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Ruch zakonczony')

    def feedback_callback(self, feedback_msg):
        pass

def main(args=None):
    rclpy.init(args=args)
    node = DobotMover()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()