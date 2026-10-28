#include <chrono>
#include <memory>
#include <thread>

#include <rclcpp/rclcpp.hpp>
#include <moveit/move_group_interface/move_group_interface.hpp>

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);

  auto node = std::make_shared<rclcpp::Node>(
    "ur5_trajectory_node",
    rclcpp::NodeOptions().automatically_declare_parameters_from_overrides(true));

  rclcpp::executors::SingleThreadedExecutor executor;
  executor.add_node(node);

  std::thread spinner([&executor]() {
    executor.spin();
  });

  int result = 0;

  try {
    RCLCPP_INFO(node->get_logger(), "Inicializando MoveGroupInterface...");

    moveit::planning_interface::MoveGroupInterface move_group(
      node, "ur_manipulator");

    move_group.setPlanningTime(10.0);
    move_group.setNumPlanningAttempts(5);
    move_group.setMaxVelocityScalingFactor(0.2);
    move_group.setMaxAccelerationScalingFactor(0.2);

    RCLCPP_INFO(node->get_logger(), "Grupo: %s",
      move_group.getName().c_str());

    RCLCPP_INFO(node->get_logger(), "Objetivo: home");

    if (!move_group.setNamedTarget("home")) {
      RCLCPP_ERROR(
        node->get_logger(),
        "No se pudo establecer el objetivo home. Verifica el SRDF.");
      result = 1;
    } else {
      moveit::planning_interface::MoveGroupInterface::Plan plan;

      RCLCPP_INFO(node->get_logger(), "Planificando trayectoria...");

      const auto planning_result = move_group.plan(plan);

      if (planning_result != moveit::core::MoveItErrorCode::SUCCESS) {
        RCLCPP_ERROR(node->get_logger(), "La planificación falló.");
        result = 2;
      } else {
        RCLCPP_INFO(
          node->get_logger(),
          "Planificación correcta. Ejecutando trayectoria...");

        const auto execution_result = move_group.execute(plan);

        if (execution_result != moveit::core::MoveItErrorCode::SUCCESS) {
          RCLCPP_ERROR(node->get_logger(), "La ejecución falló.");
          result = 3;
        } else {
          RCLCPP_INFO(
            node->get_logger(),
            "ÉXITO: MoveIt planificó y ejecutó la trayectoria.");
        }
      }
    }
  } catch (const std::exception & e) {
    RCLCPP_ERROR(
      node->get_logger(), "Excepción durante la ejecución: %s", e.what());
    result = 4;
  }

  executor.cancel();
  if (spinner.joinable()) {
    spinner.join();
  }

  rclcpp::shutdown();
  return result;
}
