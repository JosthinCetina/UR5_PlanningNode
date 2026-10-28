#!/usr/bin/env bash
set -Ee -o pipefail

WORKSPACE="${HOME}/RBTC"
LOG_DIR="${WORKSPACE}/logs/ur5_moveit"
mkdir -p "${LOG_DIR}"

PIDS=()
NAMES=()

cleanup() {
    local exit_code=$?
    trap - INT TERM EXIT
    echo
    echo "Cerrando el entorno UR5 + MoveIt..."

    for i in "${!PIDS[@]}"; do
        local pid="${PIDS[$i]}"
        if kill -0 "${pid}" 2>/dev/null; then
            echo "Deteniendo ${NAMES[$i]}..."
            kill -INT -- "-${pid}" 2>/dev/null || true
        fi
    done

    for _ in {1..10}; do
        local alive=0
        for pid in "${PIDS[@]}"; do
            kill -0 "${pid}" 2>/dev/null && alive=1
        done
        (( alive == 0 )) && break
        sleep 1
    done

    for pid in "${PIDS[@]}"; do
        if kill -0 "${pid}" 2>/dev/null; then
            kill -TERM -- "-${pid}" 2>/dev/null || true
        fi
    done

    for pid in "${PIDS[@]}"; do
        wait "${pid}" 2>/dev/null || true
    done

    echo "Registros: ${LOG_DIR}"
    exit "${exit_code}"
}

trap cleanup INT TERM
trap 'exit 1' ERR

[[ -f /opt/ros/jazzy/setup.bash ]] || {
    echo "ERROR: No se encontró ROS 2 Jazzy."
    exit 1
}
[[ -f "${WORKSPACE}/install/setup.bash" ]] || {
    echo "ERROR: No se encontró ${WORKSPACE}/install/setup.bash"
    exit 1
}

source /opt/ros/jazzy/setup.bash
source "${WORKSPACE}/install/setup.bash"
cd "${WORKSPACE}"

start_process() {
    local name="$1"
    shift
    echo "Iniciando ${name}..."
    setsid "$@" > "${LOG_DIR}/${name}.log" 2>&1 &
    local pid=$!
    PIDS+=("${pid}")
    NAMES+=("${name}")
    sleep 2
    if ! kill -0 "${pid}" 2>/dev/null; then
        echo "ERROR: ${name} terminó inesperadamente."
        tail -n 60 "${LOG_DIR}/${name}.log" || true
        exit 1
    fi
    echo "${name} iniciado (PID ${pid})."
}

wait_for_service() {
    local service="$1"
    local timeout="${2:-120}"
    local elapsed=0
    echo "Esperando servicio ${service}..."
    until ros2 service list 2>/dev/null | grep -Fxq "${service}"; do
        if (( elapsed >= timeout )); then
            echo "ERROR: Tiempo agotado esperando ${service}."
            exit 1
        fi
        sleep 2
        elapsed=$((elapsed + 2))
    done
}

wait_for_action() {
    local action="$1"
    local timeout="${2:-120}"
    local elapsed=0
    echo "Esperando acción ${action}..."
    until ros2 action list 2>/dev/null | grep -Fxq "${action}"; do
        if (( elapsed >= timeout )); then
            echo "ERROR: Tiempo agotado esperando ${action}."
            exit 1
        fi
        sleep 2
        elapsed=$((elapsed + 2))
    done
}

start_process "gazebo_bringup" \
    ros2 launch ur5_robotiq_bringup sim_gz_sgb.launch.py launch_rviz:=false

wait_for_service "/controller_manager/list_controllers" 120

echo "Esperando /joint_states..."
elapsed=0
until ros2 topic echo /joint_states --once --timeout 2 \
    >/dev/null 2>&1; do
    if (( elapsed >= 120 )); then
        echo "ERROR: No se recibió /joint_states."
        exit 1
    fi
    sleep 2
    elapsed=$((elapsed + 2))
done

start_process "move_group" \
    ros2 launch ur5_gripper_moveit_config move_group.launch.py

wait_for_action "/move_action" 120

start_process "rviz_moveit" \
    ros2 launch ur5_gripper_moveit_config moveit_rviz.launch.py

echo
echo "Entorno iniciado. Prueba Planning Group = ur_manipulator."
echo "Logs: ${LOG_DIR}"
echo "Pulsa Ctrl+C para cerrar."

while true; do
    for i in "${!PIDS[@]}"; do
        if ! kill -0 "${PIDS[$i]}" 2>/dev/null; then
            echo "ERROR: ${NAMES[$i]} terminó."
            tail -n 80 "${LOG_DIR}/${NAMES[$i]}.log" || true
            exit 1
        fi
    done
    sleep 2
done
