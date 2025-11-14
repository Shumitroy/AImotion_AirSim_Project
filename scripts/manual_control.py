
from __future__ import annotations

import time
from typing import Dict

import airsim 

from config import CONFIG


KEY_COMMANDS: Dict[str, tuple[float, float, float, float]] = {
    "w": (1.0, 0.0, 0.0, 0.0),   # forward
    "s": (-1.0, 0.0, 0.0, 0.0),  # backward
    "a": (0.0, -1.0, 0.0, 0.0),  # left
    "d": (0.0, 1.0, 0.0, 0.0),   # right
    "q": (0.0, 0.0, -1.0, 0.0),  # up
    "e": (0.0, 0.0, 1.0, 0.0),   # down
    "j": (0.0, 0.0, 0.0, -30.0), # yaw left  (deg/s)
    "l": (0.0, 0.0, 0.0, 30.0),  # yaw right
}


def _connect_client() -> airsim.MultirotorClient:
    client = airsim.MultirotorClient(ip=CONFIG.ip, port=CONFIG.port)
    client.confirmConnection()
    client.enableApiControl(True, vehicle_name=CONFIG.vehicle_name)
    client.armDisarm(True, vehicle_name=CONFIG.vehicle_name)
    return client


def run_manual_control() -> None:
    client = _connect_client()
    print("[Manual Control] Connected to AirSim.")
    print("Taking off...")
    client.takeoffAsync(vehicle_name=CONFIG.vehicle_name).join()
    client.moveToZAsync(
        CONFIG.default_altitude,
        CONFIG.default_velocity,
        vehicle_name=CONFIG.vehicle_name,
    ).join()

    print(
        "\nControls:\n"
        "  w/s = forward/backward\n"
        "  a/d = left/right\n"
        "  q/e = up/down\n"
        "  j/l = yaw left/right\n"
        "  x   = stop\n"
        "  exit = quit\n"
    )

    try:
        while True:
            cmd = input("Command: ").strip().lower()

            if cmd == "exit":
                break

            if cmd == "x":
                client.moveByVelocityBodyFrameAsync(
                    0, 0, 0, duration=0.1, vehicle_name=CONFIG.vehicle_name
                ).join()
                continue

            if cmd not in KEY_COMMANDS:
                print("Unknown command.")
                continue

            vx, vy, vz, yaw_rate = KEY_COMMANDS[cmd]

            client.moveByVelocityAsync(
                vx,
                vy,
                vz,
                duration=0.5,
                drivetrain=airsim.DrivetrainType.MaxDegreeOfFreedom,
                yaw_mode=airsim.YawMode(is_rate=True, yaw_or_rate=yaw_rate),
                vehicle_name=CONFIG.vehicle_name,
            ).join()

    finally:
        print("Landing and releasing control...")
        client.landAsync(vehicle_name=CONFIG.vehicle_name).join()
        client.armDisarm(False, vehicle_name=CONFIG.vehicle_name)
        client.enableApiControl(False, vehicle_name=CONFIG.vehicle_name)
        time.sleep(1.0)
        print("Done.")
