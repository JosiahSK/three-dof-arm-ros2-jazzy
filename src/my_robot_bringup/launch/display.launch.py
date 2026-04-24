import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
      pkg_description = get_package_share_directory('my_robot_description')
      pkg_bringup = get_package_share_directory('my_robot_bringup')

    default_model_path = os.path.join(pkg_description, 'urdf', 'arm.urdf.xacro')
    default_rviz_path = os.path.join(pkg_bringup, 'rviz', 'display.rviz')

    robot_state_publisher_node = Node(
              package='robot_state_publisher',
              executable='robot_state_publisher',
              parameters=[{
                            'robot_description': Command(['xacro ', LaunchConfiguration('model')])
              }]
    )

    joint_state_publisher_gui_node = Node(
              package='joint_state_publisher_gui',
              executable='joint_state_publisher_gui',
              name='joint_state_publisher_gui'
    )

    rviz_node = Node(
              package='rviz2',
              executable='rviz2',
              name='rviz2',
              output='screen',
              arguments=['-d', LaunchConfiguration('rvizconfig')],
    )

    return LaunchDescription([
              DeclareLaunchArgument(
                            name='model',
                            default_value=default_model_path,
                            description='Absolute path to robot URDF/xacro file'
              ),
              DeclareLaunchArgument(
                            name='rvizconfig',
                            default_value=default_rviz_path,
                            description='Absolute path to RViz config file'
              ),
              robot_state_publisher_node,
              joint_state_publisher_gui_node,
              rviz_node
    ])
