import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():
    pkg_share = get_package_share_directory('dif_bot_description')
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')

    xacro_file = os.path.join(pkg_share, 'urdf', 'dif_bot_description.urdf.xacro')
    rviz_config_file = os.path.join(pkg_share, 'rviz', 'urdf_config2.rviz')

    # 1. Sustitución de comando para procesar XACRO a URDF (compatible con la lista de arguments)
    doc = Command(['xacro ', xacro_file])

    # 2. Envoltura de parámetro (compatible EXCLUSIVAMENTE con la lista de parameters)
    robot_description_param = ParameterValue(doc, value_type=str)

    # Nodo 1: Robot State Publisher
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description_param,
            'use_sim_time': True
        }]
    )

    # Servidor de Gazebo Harmonic
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': '-r empty.sdf'}.items()
    )

    # Nodo 2: Instanciación del robot en Gazebo (utiliza doc directamente)
    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-string', doc,
            '-name', 'dif_bot',
            '-z', '0.1'
        ],
        output='screen'
    )

    # Nodo 3: Puente de comunicación ROS 2 <-> Gazebo Sim
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist',
            '/odom@nav_msgs/msg/Odometry@gz.msgs.Odometry',
            '/tf@tf2_msgs/msg/TFMessage@gz.msgs.Pose_V',
            '/joint_states@sensor_msgs/msg/JointState@gz.msgs.Model'
        ],
        output='screen'
    )

    # Nodo 4: RViz2
    node_rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_file],
        parameters=[{'use_sim_time': True}]
    )

    return LaunchDescription([
        node_robot_state_publisher,
        gazebo,
        spawn_entity,
        bridge,
        node_rviz
    ])
