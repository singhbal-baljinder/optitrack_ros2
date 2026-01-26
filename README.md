# optitrack_ros2

This is a simple implementation of a ROS 2 node that exposes Optitrack frames on a ROS 2 `PoseArray` topic. It uses **NatNet SDK 3.1** and **Motive 3.1.1**.

## :clipboard: Build Instructions

A simple way to build and manage the environment is to use **RoboStack** (Conda-based ROS 2 distribution):

1. Create the ROS 2 environment:
   ```
   conda create -n ros_env -c conda-forge -c robostack-humble ros-humble-desktop ros-dev-tools
   ```
2. Activate the environement:
   ```
   conda activate ros_env
   ```
3. Clone the repository in the ROS 2 workspace:
  ```
  mkdir -p ~/ros2_ws/src
  cd ~/ros2_ws/src
  git clone [https://github.com/singhbal-baljinder/optitrack_ros2.git](https://github.com/singhbal-baljinder/optitrack_ros2.git)
  ```
4. Build using `colcon`:
  ```
  cd ~/ros2_ws
  colcon build 
  source install/setup.bash
  ```
5. Install the NatNet client:
 ```
 cd <path-to-repo>/optitrack_ros2/NatNetSDKPython
 pip install -e .
 ```
# 🏃 Run the node
  ```
  source ~/ros2_ws/install/setup.bash
  ros2 run optitrack_ros2 optitrack_node
  ```
