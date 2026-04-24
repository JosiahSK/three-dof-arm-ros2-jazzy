import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
      pkg_share = get_package_share_directory('my_robot_description')

    robot_description_content = Command([
              PathJoinSubstitution([FindExecutable(name='xacro')]),
              ' ',
              PathJoinSubstitution([pkg_share, 'urdf', 'arm.urdf.xacro']),
    ])
    robot_description = {'robot_description': robot_description_content}

    robot_state_publisher_node = Node(
              package='robot_state_publisher',
              executable='robot_state_publisher',
              output='both',
              parameters=[robot_description, {'use_sim_time': True}]
    )

    gazebo = IncludeLaunchDescription(
              PythonLaunchDescriptionSource([
                            PathJoinSubstitution([
                                              FindPackageShare('ros_gz_sim'),
                                              'launch',
                                              'gz_sim.launch.py'
                            ])
              ]),
              launch_arguments={'gz_args': '-r empty.sdf'}.items()
    )

    gz_spawn_entity = Node(
              package='ros_gz_sim',
              executable='create',
              output='screen',
              arguments=['-topic', 'robot_description', '-name', 'my_robot', '-allow_renaming', 'true'],
    )

    bridge = Node(
              package='ros_gz_bridge',
              executable='parameter_bridge',
              arguments=['/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock'],
              output='screen'
    )

    joint_state_broadcaster_spawner = Node(
              package='controller_manager',
              executable='spawner',
              arguments=['joint_state_broadcaster', '--controller-manager', '/controller_manager'],
    )

    arm_controller_spawner = Node(
              package='controller_manager',
              executable='spawner',
              arguments=['arm_controller', '-c', '/controller_manager'],
    )

    gripper_controller_spawner = Node(
              package='controller_manager',
              executable='spawner',
              arguments=['gripper_controller', '-c', '/controller_manager'],
    )

    return LaunchDescription([
              robot_state_publisher_node,
              gazebo,
              bridge,
              gz_spawn_entity,
              joint_state_broadcaster_spawner,
              arm_controller_spawner,
              gripper_controller_spawner,
    ])
