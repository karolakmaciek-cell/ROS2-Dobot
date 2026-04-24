import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from dobot_msgs.action import PointToPoint
from dobot_msgs.srv import GripperControl
from typing import List

OVERHEAD = 75
HEIGHT_INCREMENT = 20

class PickAndPlaceNode(Node):
    def __init__(self):
        super().__init__('dobot_controller')
        self.declare_parameter('tower_height', 3)
        self.tower_height = self.get_parameter('tower_height').value
        self.tower_height = self.get_parameter('tower_height').get_parameter_value().integer_value

        self.ptp_client = ActionClient(self, PointToPoint, '/PTP_action')
        self.gripper_client = self.create_client(GripperControl, '/dobot_gripper_service')

                                        #X          $Y      #Z      #PHI
        self.tower_pick_params: List = [[206.772, -98.586, 11.654, -43.141],
                                        [179.781, -95.189, 7.32, -46.716],
                                        [152.173, -95.785, 8.531, -51.004]
                                        ]
        
        self.tower_place_params = [184.525, 73.355, 7.085, 2.943]

    def move_to_xyz(self, x: float, y: float, z: float, phi: float):
        self.get_logger().info('Movement start')
        goal_msg = PointToPoint.Goal()
        goal_msg.motion_type = 1
        goal_msg.target_pose = [x, y, z, phi]
        goal_msg.velocity_ratio = 0.3
        goal_msg.acceleration_ratio = 0.3
        self.get_logger().info('Movement end')
        
        self.ptp_client.wait_for_server()
        
        send_goal_future = self.ptp_client.send_goal_async(goal_msg)
        rclpy.spin_until_future_complete(self, send_goal_future)
        
        goal_handle = send_goal_future.result()
        if goal_handle.accepted:
            result_future = goal_handle.get_result_async()
            rclpy.spin_until_future_complete(self, result_future)

    def controll_gripper(self, state, comp):
        self.get_logger().info('Gripper start')
        self.gripper_client.wait_for_service()
        req = GripperControl.Request()
        req.gripper_state = state
        req.keep_compressor_running = comp
        
        future = self.gripper_client.call_async(req)
        rclpy.spin_until_future_complete(self, future)
        self.get_logger().info('Gripper end')

    def pick_and_place(self, x_pick: float, y_pick: float, z_pick: float, phi_pick: float,
                        x_place: float, y_place: float, z_place: float, phi_place: float):
        
        self.move_to_xyz(x_pick, y_pick, z_pick + OVERHEAD, phi_pick)
        self.move_to_xyz(x_pick, y_pick, z_pick, phi_pick)
        self.controll_gripper('close', True)
        self.move_to_xyz(x_pick, y_pick, z_pick + OVERHEAD, phi_pick)
        self.move_to_xyz(x_place, y_place, z_place + OVERHEAD, phi_place)
        self.move_to_xyz(x_place, y_place, z_place, phi_place)
        self.controll_gripper('open', False)
        self.move_to_xyz(x_place, y_place, z_place + OVERHEAD, phi_place)

def main(args=None):
    rclpy.init(args=args)
    node = PickAndPlaceNode()
    
    try:
        for i in range(node.tower_height):
            x_pick = node.tower_pick_params[i][0]
            y_pick = node.tower_pick_params[i][1]
            z_pick = node.tower_pick_params[i][2]
            phi_pick = node.tower_pick_params[i][3]

            x_place = node.tower_place_params[0]
            y_place = node.tower_place_params[1]
            z_place = node.tower_place_params[2] + i * HEIGHT_INCREMENT
            phi_place = node.tower_place_params[3]
            
            node.pick_and_place(x_pick, y_pick, z_pick, phi_pick, 
                                x_place, y_place, z_place, phi_place)
    
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()