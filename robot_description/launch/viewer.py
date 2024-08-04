import launch
from launch.substitutions import Command, LaunchConfiguration
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
import launch_ros
import os

def generate_launch_description():
    robot_description_pkg_path = launch_ros.substitutions.FindPackageShare(package='robot_description').find('robot_description')
    mapping_gazebo_pkg_path = launch_ros.substitutions.FindPackageShare(package="mapping_gazebo").find('mapping_gazebo')
    mapping_bringup_pkg_path = launch_ros.substitutions.FindPackageShare(package="mapping_bringup").find('mapping_bringup')
    ros_gz_sim_pkg_path = launch_ros.substitutions.FindPackageShare(package="ros_gz_sim").find('ros_gz_sim')

    sdfModelPath= os.path.join(robot_description_pkg_path, 'models/firebird_vi/model.sdf')
    
    with open(sdfModelPath,'r') as infp:
    	robot_desc = infp.read()

    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim_pkg_path, 'launch', 'gz_sim.launch.py')),
        launch_arguments={'gz_args': PathJoinSubstitution([
            mapping_gazebo_pkg_path,
            'worlds',
            'empty.sdf'
        ])}.items(),
    )

    joint_state_publisher_gui = launch_ros.actions.Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        arguments=[sdfModelPath],
        output=['screen']
    )
    
    robot_state_publisher_node = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='both',
        parameters=[
            {'use_sim_time': True},
            {'robot_description': robot_desc},
        ]
    )
    
    rviz_node = launch_ros.actions.Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen'
    )

    bridge_node = launch_ros.actions.Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{
            'config_file': os.path.join(mapping_bringup_pkg_path, 'config', 'ros_gz_bridge.yaml'),
        }],
        output='screen'
    )

    return launch.LaunchDescription([
        launch.actions.DeclareLaunchArgument(name='model', default_value=sdfModelPath,
                                            description='Path to the sdf model file'),
        gz_sim,
        joint_state_publisher_gui,
        robot_state_publisher_node,
        rviz_node,
        bridge_node
    ]) 