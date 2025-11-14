
import argparse

from scripts.manual_control import run_manual_control
from scripts.stable_velocity import run_stable_velocity_demo
from scripts.adaptive_camera import run_adaptive_camera_demo


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AirSim Project Launcher")
    parser.add_argument(
        "--mode",
        type=str,
        choices=["manual", "stable", "adaptive_cam"],
        required=True,
        help="Which demo to run.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.mode == "manual":
        run_manual_control()
    elif args.mode == "stable":
        run_stable_velocity_demo()
    elif args.mode == "adaptive_cam":
        run_adaptive_camera_demo()
    else:
        raise ValueError(f"Unknown mode: {args.mode}")


if __name__ == "__main__":
    main()
