# AImotion_AirSim_Project
# Autonomous Drone Simulation Platform (AirSim + Unreal Engine) 
# Autonomous drone navigation in GPS denied area

A modular, high-fidelity drone simulation framework built on **Microsoft AirSim** and **Unreal Engine**.  
Designed for research and engineering in autonomous flight, adaptive perception, and AI-driven navigation.

This project provides a clean foundation for experimenting with control systems, dataset generation, and deep-learning–based end-to-end navigation in simulation.

---



## 🚀 Key Features

### **🔹 High-Fidelity Simulation**
- Integrates with Microsoft **AirSim**
- Supports custom **Unreal Engine** environments (urban, forest, indoor)
- Configurable camera models (FOV, resolution, framerate)
- Realistic physics & sensor noise

### **🔹 Modular Flight Control**
- `manual_control.py` — Keyboard-driven control for debugging
- `stable_velocity.py` — Constant velocity flight for dataset creation
- `adaptive_camera.py` — Dynamic camera pipeline adjusting to drone speed/motion

### **🔹 AI / ML Integration**
- `navigation_cnn.py` — Starter CNN for vision-based navigation
- Extensible to RL, imitation learning, SLAM, and control policies
- Clean input/output interfaces for training pipelines

### **🔹 Clean Code Architecture**
- Centralized config (`config.py`)
- Modular scripts in `scripts/`
- Model architectures in `models/`
- Ready for scaling into a full autonomy stack

---

## 📁 Repository Structure

```
AirSim_Project/
│
├── main.py                   # Entry point for all modes
├── config.py                 # Central configuration
│
├── scripts/
│   ├── manual_control.py     # Manual flight control
│   ├── stable_velocity.py    # Constant-speed flight
│   └── adaptive_camera.py    # Dynamic camera system
│
└── models/
    └── navigation_cnn.py     # CNN for end-to-end navigation
```

---

## 🧪 Usage

Before running, make sure:
- AirSim is running  
- You installed dependencies (`pip install -r requirements.txt`)

### **Manual Control**
```bash
python main.py --mode manual
python main.py --mode stable
python main.py --mode adaptive_cam
pip install -r requirements.txt

### Requires:

Python 3.8+

Microsoft AirSim

Unreal Engine environment or AirSim Blocks environment

This repository serves as a foundation for:

Autonomous drone navigation in GPS denied area

Reinforcement learning in simulation

Adaptive perception systems

High-quality dataset generation

Real-to-sim and sim-to-real research

AI-driven robotics prototyping

The project is designed to grow into a fully customizable autonomy research environment.

