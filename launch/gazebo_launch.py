import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    pkg_name = 'project_a_description'
    pkg_share = get_package_share_directory(pkg_name)
    world_file = os.path.join(pkg_share, 'worlds', 'site.world')
    
    # For model:// URI resolution (both models/ and package root)
    models_path = os.path.join(pkg_share, 'models')
    
    # Also add package share for mesh references in embedded world
    # Gazebo searches all paths in GAZEBO_MODEL_PATH for model:// URIs
    gazebo_model_path = models_path + ':' + pkg_share

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
        launch_arguments={'world': world_file}.items()
    )

    urdf_file = os.path.join(pkg_share, 'urdf', 'construction_robot.urdf')
    with open(urdf_file, 'r') as infp:
        robot_desc = infp.read()
    
    rsp = Node(
        package='robot_state_publisher', 
        executable='robot_state_publisher',
        output='screen', 
        parameters=[{'robot_description': robot_desc}]
    )

    spawn_robot = Node(
        package='gazebo_ros', 
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description', 
                   '-entity', 'construction_robot', 
                   '-x', '2.0', '-y', '2.0', '-z', '1.0'],
        output='screen'
    )

    return LaunchDescription([
        SetEnvironmentVariable(name='GAZEBO_MODEL_PATH', value=gazebo_model_path),
        SetEnvironmentVariable(name='LIBGL_ALWAYS_SOFTWARE', value='1'),
        gazebo,
        rsp,
        TimerAction(period=5.0, actions=[spawn_robot])
    ])