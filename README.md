# BIM-Integrated Autonomous Mobile Robot (AMR) Simulation 🏗️🤖


![Status](https://img.shields.io/badge/Status-In--Progress-orange)
![ROS2](https://img.shields.io/badge/ROS2-Humble-blue)
![Gazebo](https://img.shields.io/badge/Simulator-Gazebo-green)

## 🚧 Work in Progress
This project is currently in active development. 

![Simulation Preview](project_a_description/assets/simulation_preview.png)

I am currently transitioning from the **Environment & Kinematics** phase to the **Sensor Integration** phase.

## 📌 Project Overview
This repository hosts a ROS2-based Digital Twin simulation designed for the construction industry. The goal is to simulate an Autonomous Mobile Robot (AMR) navigating a high-fidelity **BIM (Building Information Modeling)** environment.

The project bridges the gap between architectural design and robotics by importing complex `.dae` meshes into a physics-driven Gazebo world.

## 🛠️ Current Features
- **BIM Integration:** Successful loading of large-scale (100MB+) architectural models with collision physics.
- **Robot Kinematics:** A custom-designed differential drive rover with a functional caster wheel.
- **Control System:** Integrated `gazebo_ros_diff_drive` plugin for real-time teleoperation.
- **ROS2 Architecture:** Clean package structure following industrial standards (URDF, SDF, and Launch logic).

## 🚀 How to Run (Development)
1. Build the workspace:

   colcon build --packages-select project_a_description
   source install/setup.bash

2. Launch the simulation:

    ros2 launch project_a_description gazebo_launch.py

📅 Roadmap

[x] Integrate BIM Mesh into Gazebo

[x] Configure Differential Drive Kinematics

[ ] Add Lidar sensor (Phase 3)

[ ] Implement SLAM for mapping the BIM site

[ ] Autonomous Waypoint Navigation