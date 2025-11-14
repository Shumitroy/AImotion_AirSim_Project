"""
Prototype of an adaptive camera pipeline.

For now:
 - Changes resolution and FOV based on speed.
 - Captures a few images at each setting.

Later you can connect this logic to a learned policy or RL agent.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Tuple

import airsim  # type: ignore
import numpy as np

from config import CONFIG


def _connect_client() -> airsim.MultirotorClient:
    client = airsim.MultirotorClient(ip=CONFIG.ip, port=CONFIG.port)
    client.confirmConnection()
    client.enableApiControl(True, vehicle_name=CONFIG.vehicle_name)
    client.armDisarm(True, vehicle_name=CONFIG.vehicle_name)
    return client


def _ensure_output_dir() -> Path:
    path = Path("data/adaptive_camera")
    path.mkdir(parents=True, exist_ok=True)
    return path


def _set_camera(
    client: airsim.MultirotorClient,
    resolution: Tuple[int, int],
    fov_degrees: float,
) -> None:
    width, height = resolution
    camera_name = CONFIG.camera_name
    vehicle_name = CONFIG.vehicle_name

    client.simSetCameraFov(fov_degrees, camera_name=camera_name, vehicle_name=vehicle_name)
    client.simSetCameraResolution(
        camera_name=camera_name,
        width=width,
        height=height,
        vehicle_name=vehicle_name,
    )


def _capture_image(
    client: airsim.MultirotorClient,
    idx: int,
    resolution: Tuple[int, int],
    speed_label: str,
) -> None:
    out_dir = _ensure_output_dir()
    responses = client.simGetImages(
        [
            airsim.ImageRequest(
                camera_name=CONFIG.camera_name,
                image_type=airsim.ImageType.Scene,
                pixels_as_float=False,
                compress=False,
            )
        ],
        vehicle_name=CONFIG.vehicle_name,
    )

    if not responses:
        print("No image received.")
        return

    img = responses[0]
    img1d = np.frombuffer(img.image_data_uint8, dtype=np.uint8)
    img_rgba = img1d.reshape(img.height, img.width, 3)

    filename = out_dir / f"{speed_label}_idx{idx}_w{img.width}_h{img.height}.png"
    airsim.write_png(os.fspath(filename), img_rgba)
    print(f"Saved {filename}")


def run_adaptive_camera_demo() -> None:
    client = _connect_client()
    print("[Adaptive Camera] Connected to AirSim.")

    client.takeoffAsync(vehicle_name=CONFIG.vehicle_name).join()
    client.moveToZAsync(
        CONFIG.default_altitude,
        CONFIG.default_velocity,
        vehicle_name=CONFIG.vehicle_name,
    ).join()

    # Example: two "speed regimes" with different camera settings.
    regimes = [
        {
            "speed": 1.0,  # slow
            "resolution": (640, 480),
            "fov": 70.0,
            "label": "slow",
        },
        {
            "speed": 6.0,  # fast
            "resolution": (320, 240),
            "fov": 110.0,
            "label": "fast",
        },
    ]

    for regime in regimes:
        v = regime["speed"]
        res = regime["resolution"]
        fov = regime["fov"]
        label = regime["label"]

        print(f"\n[Regime: {label}] speed={v}, res={res}, fov={fov}")
        _set_camera(client, res, fov)

        # Move straight for a bit while capturing images.
        client.moveByVelocityAsync(
            v,
            0.0,
            0.0,
            duration=2.0,
            drivetrain=airsim.DrivetrainType.MaxDegreeOfFreedom,
            yaw_mode=airsim.YawMode(is_rate=False, yaw_or_rate=0.0),
            vehicle_name=CONFIG.vehicle_name,
        ).join()

        for i in range(3):
            _capture_image(client, idx=i, resolution=res, speed_label=label)

    client.hoverAsync(vehicle_name=CONFIG.vehicle_name).join()
    client.landAsync(vehicle_name=CONFIG.vehicle_name).join()
    client.armDisarm(False, vehicle_name=CONFIG.vehicle_name)
    client.enableApiControl(False, vehicle_name=CONFIG.vehicle_name)
    print("\nAdaptive camera demo finished.")
