import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():
    pkg_share = get_package_share_directory('dif_bot_description')
    
    # Rutas absolutas resueltas desde el directorio share del paquete
    xacro_file = os.path.join(pkg_share, 'urdf', 'dif_bot_description.urdf.xacro')
    rviz_config_file = os.path.join(pkg_share, 'rviz', 'urdf_config2.rviz')

    # Envoltura explicita para forzar la interpretacion de XML como cadena de texto (str)
    robot_description_content = ParameterValue(
        Command(['xacro ', xacro_file]),
        value_type=str
    )
    
    robot_description = {'robot_description': robot_description_content}

    # Nodo 1: Robot State Publisher
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description]
    )

    # Nodo 2: Joint State Publisher GUI
    node_joint_state_publisher_gui = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        output='screen'
    )

    # Nodo 3: RViz2 con carga directa del archivo de configuracion urdf_config.rviz
    node_rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_file]
    )

    return LaunchDescription([
        node_robot_state_publisher,
        node_joint_state_publisher_gui,
        node_rviz
    ])
