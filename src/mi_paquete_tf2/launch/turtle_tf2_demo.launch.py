import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # Node 1: Simulador principal
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='sim'
        ),
        # Node 2: Broadcaster para turtle1
        Node(
            package='mi_paquete_tf2',
            executable='turtle_tf2_broadcaster',
            name='broadcaster1',
            parameters=[{'turtlename': 'turtle1'}]
        ),
        # Service call: Generar turtle2
        ExecuteProcess(
            cmd=['ros2', 'service', 'call', '/spawn', 'turtlesim/srv/Spawn',
                 '"{x: 2.0, y: 2.0, theta: 0.0, name: \'turtle2\'}"'],
            shell=True
        ),
        # Node 3: Broadcaster para turtle2
        Node(
            package='mi_paquete_tf2',
            executable='turtle_tf2_broadcaster',
            name='broadcaster2',
            parameters=[{'turtlename': 'turtle2'}]
        ),
        # Node 4: Broadcaster del nuevo marco fijo (carrot1)
        Node(
            package='mi_paquete_tf2',
            executable='fixed_frame_tf2_broadcaster',
            name='broadcaster_fixed'
        ),
        # Node 5: Listener asignado por defecto a carrot1
        Node(
            package='mi_paquete_tf2',
            executable='turtle_tf2_listener',
            name='listener',
            parameters=[{'target_frame': 'carrot1'}]
        ),
    ])
