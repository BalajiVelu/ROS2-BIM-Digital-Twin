import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Path to your package
    pkg_share = get_package_share_directory('project_a_description')
    
    # Include your existing Gazebo launch (spawns robot + world)
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_share, 'launch', 'gazebo_launch.py')
        )
    )
    
    # SLAM Toolbox node (online synchronous mode)
    slam_toolbox = Node(
        package='slam_toolbox',
        executable='async_slam_toolbox_node',
        name='slam_toolbox',
        output='screen',
        parameters=[
            {
                'use_sim_time': True,
                'max_laser_range': 10.0,
                'minimum_time_interval': 0.5,
                'transform_timeout': 0.2,
                'tf_buffer_duration': 30.0,
                'stack_size_to_use': 40000000,
                'enable_interactive_mode': True,
                'solver_plugin': 'solver_plugins::CeresSolver',
                'ceres_linear_solver': 'sparse_schur',
                'ceres_preconditioner': 'schur_jacobi',
                'ceres_trust_strategy': 'levenberg_marquardt',
                'ceres_dogleg_type': 'traditional_dogleg',
                'ceres_loss_function': 'None',
                'odom_frame': 'odom',
                'map_frame': 'map',
                'base_frame': 'base_footprint',
                'scan_topic': '/scan',
                'mode': 'mapping',
            }
        ],
        remappings=[
            ('/scan', '/scan'),
        ]
    )
    
    # RViz2 with SLAM configuration
    rviz2 = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', os.path.join(pkg_share, 'rviz', 'slam.rviz')],
        condition=LaunchConfiguration('rviz', default='true')
    )
    
    return LaunchDescription([
        gazebo_launch,
        slam_toolbox,
        rviz2,
    ])