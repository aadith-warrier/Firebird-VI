# Firebird VI

This is a ROS2 library for simulating the [Firebrid VI](http://www.nex-robotics.com/products/fire-bird-vi-robot.html) robot from NEX Robotics. 

---

![Visual Slam using RTAB Mapping](assets/png/vslam.png)

# System Bringup for Robot Simulation and Navigation

To set up and bring up various nodes in the robot's environment, follow the sequence of steps below. Each step is crucial for initializing different components, from the Gazebo simulator to the SLAM and navigation systems.

## Step 1: Launch the Gazebo Simulator and Robot Model

Start the Gazebo simulation environment along with the robot model. This will initialize the virtual robot in the simulated environment.

```bash
ros2 launch robot_description viewer.py
```

## Step 2: Initialize Odometry and Static Transforms
This step brings up essential mapping nodes, including odometry and static transformations, which are foundational for localization and path planning.

```bash 
ros2 launch ./src/mapping_bringup/launch/basic.launch
```

## Step 3: Launch SLAM (Simultaneous Localization and Mapping)
To enable SLAM, run the following command. SLAM is responsible for building a map of the environment while tracking the robot's position within it.

```bash
ros2 launch ./src/mapping_bringup/launch/firebird_slam.launch
```

## Step 4: Start Nav2 Navigation Stack
Initialize the Nav2 navigation stack with the specified parameter file. This will enable autonomous navigation capabilities.

```bash
ros2 launch nav2_bringup navigation_launch.py params_file:=./src/firebird_navigation/config/nav2_params.yaml
```