"""
Central configuration for the AirSim project.
Adjust these values to match your setup.
"""

from dataclasses import dataclass


@dataclass
class AirSimConfig:
    # Connection
    ip: str = "127.0.0.1"
    port: int = 41451

    # Vehicle
    vehicle_name: str = "Drone1"

    # Camera
    camera_name: str = "0"
    image_width: int = 640
    image_height: int = 480
    fov_degrees: float = 90.0

    # Flight defaults
    default_altitude: float = -5.0  # NED frame: negative z is up
    default_velocity: float = 3.0   # m/s


CONFIG = AirSimConfig()
