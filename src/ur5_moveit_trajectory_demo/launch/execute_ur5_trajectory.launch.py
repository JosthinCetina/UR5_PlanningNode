from launch import LaunchDescription
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder


def generate_launch_description():
    moveit_config = (
        MoveItConfigsBuilder(
            "ur",
            package_name="ur5_gripper_moveit_config"
        ).to_moveit_configs()
    )

    trajectory_node = Node(
        package="ur5_moveit_trajectory_demo",
        executable="ur5_trajectory_node",
        name="ur5_trajectory_node",
        output="screen",
        parameters=[
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.robot_description_kinematics,
            moveit_config.planning_pipelines,
            moveit_config.joint_limits,
            {"use_sim_time": True},
        ],
    )

    return LaunchDescription([trajectory_node])
