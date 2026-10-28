from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import SetParameter
from moveit_configs_utils import MoveItConfigsBuilder
from moveit_configs_utils.launches import generate_move_group_launch

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time')
    
    moveit_config = MoveItConfigsBuilder("ur", package_name="ur5_gripper_moveit_config").to_moveit_configs()
    
    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true', description='Use simulation (Gazebo) clock'),
        SetParameter(name='use_sim_time', value=use_sim_time),
        generate_move_group_launch(moveit_config)
    ])
