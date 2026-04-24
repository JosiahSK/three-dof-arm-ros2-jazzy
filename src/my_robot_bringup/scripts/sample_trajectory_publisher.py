#!/usr/bin/env python3
"""
sample_trajectory_publisher.py
Publishes sample JointTrajectory messages to test ros2_control.
Run AFTER gazebo.launch.py and controllers are active.
"""

import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration
import math


class SampleTrajectoryPublisher(Node):

      def __init__(self):
                super().__init__('sample_trajectory_publisher')
                self.arm_pub = self.create_publisher(
                    JointTrajectory, '/arm_controller/joint_trajectory', 10)
                self.gripper_pub = self.create_publisher(
                    JointTrajectory, '/gripper_controller/joint_trajectory', 10)
                self.timer = self.create_timer(3.0, self.publish_trajectory)
                self.step = 0
                self.get_logger().info('SampleTrajectoryPublisher started!')

      def publish_trajectory(self):
                arm_msg = JointTrajectory()
                arm_msg.joint_names = ['joint1', 'joint2', 'joint3']
                gripper_msg = JointTrajectory()
                gripper_msg.joint_names = ['gripper_joint']
                point = JointTrajectoryPoint()
                gripper_point = JointTrajectoryPoint()
                if self.step % 2 == 0:
                              point.positions = [0.0, -math.pi / 4, math.pi / 4]
                              gripper_point.positions = [0.02]
                              self.get_logger().info('Position A: arm forward, gripper open')
else:
            point.positions = [math.pi / 2, -math.pi / 3, math.pi / 6]
              gripper_point.positions = [-0.02]
            self.get_logger().info('Position B: arm side, gripper closed')
        point.time_from_start = Duration(sec=2, nanosec=0)
        gripper_point.time_from_start = Duration(sec=2, nanosec=0)
        arm_msg.points = [point]
        gripper_msg.points = [gripper_point]
        self.arm_pub.publish(arm_msg)
        self.gripper_pub.publish(gripper_msg)
        self.step += 1


def main(args=None):
      rclpy.init(args=args)
    node = SampleTrajectoryPublisher()
    try:
              rclpy.spin(node)
except KeyboardInterrupt:
        pass
finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
      main()
