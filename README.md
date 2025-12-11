# TB3 GUI - TurtleBot3 Graphical User Interface

A ROS2 (Robot Operating System 2) project providing graphical user interfaces for controlling and monitoring TurtleBot3 robots.

## Overview

This project contains multiple packages for interfacing with TurtleBot3 robots through ROS2:

- **tb3_gui**: Python-based GUI using PyQt5 for robot control and visualization

## Features

### tb3_gui (Python + PyQt5)
- **Real-time Odometry Display**: Shows current robot position (x, y coordinates)
- **Live Camera Feed**: Real-time camera stream from robot
- **Two-Column Layout**: Organized interface with plots on left, camera on right
- **Velocity Control**: Arrow key buttons for intuitive robot movement
- **Speed Control**: Adjustable sliders for linear and angular velocities
- **Live Velocity Graphs**: Real-time visualization of linear and angular velocities
- **Trajectory Mapping**: Interactive plot showing robot's movement path
- **Professional UI**: Dark theme with industrial-style controls

## Prerequisites

- **ROS2** (Humble or later recommended)
- **Python 3.8+**
- **PyQt5** (for tb3_gui)
- **TurtleBot3 packages** for ROS2

### Dependencies

```bash
# For tb3_gui
pip install PyQt5 matplotlib numpy opencv-python

# For ROS2
sudo apt install ros-humble-desktop
sudo apt install ros-humble-turtlebot3*
sudo apt install ros-humble-cv-bridge
```

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd ros_tb3
   ```

2. **Build the packages:**
   ```bash
   colcon build
   ```

3. **Source the workspace:**
   ```bash
   source install/setup.bash
   ```

## Usage

### Running the Python GUI

```bash
# Terminal 1: Launch TurtleBot3 simulation
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py

# Terminal 2: Run the GUI
ros2 run tb3_gui tb3_gui_node
```

## GUI Layout

The GUI features a professional three-section layout:

### Header Section
- **Odometry Display**: Real-time robot position coordinates

### Main Section (Two-Column Layout)
#### Left Column - Data Visualization
- **Velocity Graph**: Real-time linear and angular velocity plots
- **Trajectory Plot**: Interactive map showing robot's movement path

#### Right Column - Camera Feed
- **Live Camera Stream**: Real-time video feed from robot's camera

### Control Section (Bottom)
- **Movement Controls**: Arrow key buttons (↑↓←→) for intuitive robot control
- **Emergency Stop**: Red STOP button for immediate halt
- **Speed Adjustment**: Sliders for linear and angular velocity tuning
- **Trajectory Management**: Clear trajectory data button

## GUI Controls

### Movement Controls
- **↑ (Forward)**: Move robot forward at selected linear speed
- **↓ (Backward)**: Move robot backward at selected linear speed
- **← (Left)**: Rotate robot counter-clockwise at selected angular speed
- **→ (Right)**: Rotate robot clockwise at selected angular speed
- **STOP**: Immediately halt all robot movement

### Speed Adjustment
- **Linear Speed Slider**: Controls forward/backward movement speed (0-1.0 m/s)
- **Angular Speed Slider**: Controls rotation speed (0-1.0 rad/s)

### Visualization Controls
- **Clear Trajectory**: Reset trajectory plot and path history

### Real-time Displays
- **Odometry Display**: Current position coordinates (x, y)
- **Velocity Graph**: Live linear and angular velocity visualization
- **Trajectory Plot**: Cumulative movement path mapping
- **Camera Feed**: Live video stream from robot

## Project Structure

```
ros_tb3/
├── src/
│   ├── tb3_gui/              # Python GUI package
│       ├── package.xml
│       ├── setup.py
│       └── tb3_gui/
│           └── tb3_gui_node.py
├── build/                    # Build artifacts (ignored)
├── install/                  # Installation files (ignored)
├── log/                      # Log files (ignored)
├── .gitignore
└── README.md
```

## ROS2 Topics

### Subscribed Topics
- `/odom` (nav_msgs/Odometry): Robot odometry information
- `/camera/image_raw/compressed` (sensor_msgs/CompressedImage): Camera feed from robot

### Published Topics
- `/cmd_vel` (geometry_msgs/Twist): Velocity commands to robot

## Development

### Building from Source

```bash
# Clean build
rm -rf build/ install/ log/
colcon build --cmake-clean-cache
```

### Testing

```bash
colcon test
colcon test-result --verbose
```

### Code Formatting

```bash
# Python
black src/tb3_gui/
flake8 src/tb3_gui/
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the [LICENSE] - see the LICENSE file for details.

## Acknowledgments

- Built for TurtleBot3 platform
- Uses ROS2 for robot communication
- PyQt5 for Python GUI development
- Matplotlib for data visualization

**Note**: This project is designed for ROS2 and TurtleBot3. Make sure you have the appropriate TurtleBot3 packages installed before running.
