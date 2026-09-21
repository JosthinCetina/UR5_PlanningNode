from launch import LaunchDescription
from launch.actions import (DeclareLaunchArgument, EmitEvent, ExecuteProcess,
                            LogInfo, RegisterEventHandler, TimerAction)
from launch.conditions import IfCondition
from launch.event_handlers import (OnExecutionComplete, OnProcessExit, OnProcessStart)
from launch.events import Shutdown
from launch.substitutions import (EnvironmentVariable, FindExecutable,
                                  LaunchConfiguration, PythonExpression)
from launch_ros.actions import Node

def generate_launch_description():
    turtlesim_ns = LaunchConfiguration("turtlesim_ns")
    use_provided_red = LaunchConfiguration("use_provided_red")
    new_background_r = LaunchConfiguration("new_background_r")

    turtlesim_ns_launch_arg = DeclareLaunchArgument(
        "turtlesim_ns", default_value="turtlesim1"
    )
    use_provided_red_launch_arg = DeclareLaunchArgument(
        "use_provided_red", default_value="False"
    )
    new_background_r_launch_arg = DeclareLaunchArgument(
        "new_background_r", default_value="200"
    )

    turtlesim_node = Node(
        package="turtlesim",
        namespace=turtlesim_ns,
        executable="turtlesim_node",
        name="sim"
    )

    spawn_turtle = ExecuteProcess(
        cmd=[
            FindExecutable(name="ros2"),
            "service", "call",
            [turtlesim_ns, "/spawn"],
            "turtlesim/srv/Spawn",
            "{x: 2.0, y: 2.0, theta: 0.2}"
        ]
    )

    set_bg_param = ExecuteProcess(
        condition=IfCondition(
            PythonExpression([
                new_background_r, " == 200 and ", use_provided_red
            ])
        ),
        cmd=[
            FindExecutable(name="ros2"),
            "param", "set",
            [turtlesim_ns, "/sim"],
            "background_r",
            new_background_r
        ]
    )

    clear_canvas = ExecuteProcess(
        condition=IfCondition(
            PythonExpression([
                new_background_r, " == 200 and ", use_provided_red
            ])
        ),
        cmd=[
            FindExecutable(name="ros2"),
            "service", "call",
            [turtlesim_ns, "/clear"],
            "std_srvs/srv/Empty",
            "{}"
        ]
    )

    return LaunchDescription([
        turtlesim_ns_launch_arg,
        use_provided_red_launch_arg,
        new_background_r_launch_arg,
        turtlesim_node,
        RegisterEventHandler(
            OnProcessStart(
                target_action=turtlesim_node,
                on_start=[
                    LogInfo(msg="Turtlesim iniciado, generando tortuga..."),
                    spawn_turtle
                ]
            )
        ),
        RegisterEventHandler(
            OnExecutionComplete(
                target_action=spawn_turtle,
                on_completion=[
                    LogInfo(msg="Spawn finalizado"),
                    TimerAction(
                        period=2.0,
                        actions=[set_bg_param, clear_canvas],
                    )
                ]
            )
        ),
        RegisterEventHandler(
            OnProcessExit(
                target_action=turtlesim_node,
                on_exit=[
                    LogInfo(msg=(EnvironmentVariable(name="USER"), " cerro la ventana de turtlesim")),
                    EmitEvent(event=Shutdown(reason="Ventana cerrada"))
                ]
            )
        )
    ])
