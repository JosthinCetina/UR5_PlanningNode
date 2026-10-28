# UR5 + Robotiq 2F-85 — ROS 2 Jazzy and MoveIt 2

Simulation and trajectory-planning project for a UR5 robot with a
Robotiq 2F-85 gripper using ROS 2 Jazzy, Gazebo and MoveIt 2.

## Repository contents

- `src/ur5_gripper_moveit_config/`: MoveIt configuration package
  generated and configured with MoveIt Setup Assistant.
- `src/ur5_gripper_packages/ur5_robotiq_bringup/`: simulation
  bringup, robot integration and controller configuration.
- `src/ur5_moveit_trajectory_demo/`: C++ node that plans and
  executes a trajectory through MoveIt 2.

## Requirements

- Ubuntu 24.04
- ROS 2 Jazzy
- Gazebo and the simulation dependencies used by the bringup package
- MoveIt 2 and the dependencies declared by the project packages

## Build

Open a terminal in the workspace root:

```bash
source /opt/ros/jazzy/setup.bash
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

## Launch the simulation and MoveIt

Start the complete simulation environment:

```bash
source /opt/ros/jazzy/setup.bash
source install/setup.bash
./ur5_moveit.sh
```

The launch script starts Gazebo, the controllers, MoveIt and RViz.

## Execute a trajectory from a ROS 2 node

With the simulation and MoveIt running, open a second terminal:

```bash
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 launch ur5_moveit_trajectory_demo execute_ur5_trajectory.launch.py
```

The demo node uses MoveGroupInterface, selects `ur_manipulator`,
plans to the named target `home`, and requests execution through MoveIt.

## Validation

The arm controller must be active, and the trajectory action must be
available for execution. A successful run should report successful
planning and execution in the node logs.

## Notes

Generated build and install artifacts are excluded from version control.
Check package licenses and third-party model/mesh redistribution
permissions before publishing this repository.
