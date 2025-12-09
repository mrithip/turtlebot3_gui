#!/usr/bin/env python3
import sys
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QSlider
from PyQt5.QtCore import QTimer, Qt
from geometry_msgs.msg import Twist
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from collections import deque

class RobotGuiNode(Node):
    def __init__(self):
        super().__init__('robot_gui_node')
        self.sub_odom = self.create_subscription(
            Odometry, '/odom', self.odom_callback, 10)
        self.pub_cmd = self.create_publisher(Twist, '/cmd_vel', 10)
        self.x = 0.0
        self.y = 0.0
        self.linear_velocity = 0.0
        self.angular_velocity = 0.0
        self.trajectory = []  # store (x, y) positions

    def odom_callback(self, msg):
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y
        self.linear_velocity = msg.twist.twist.linear.x
        self.angular_velocity = msg.twist.twist.angular.z
        self.trajectory.append((self.x, self.y))

    def move(self, linear_x=0.0, angular_z=0.0):
        msg = Twist()
        msg.linear.x = linear_x
        msg.angular.z = angular_z
        self.pub_cmd.publish(msg)

    def stop(self):
        self.move(0.0, 0.0)

class GuiWindow(QWidget):
    def __init__(self, node):
        super().__init__()
        self.node = node
        self.setWindowTitle("TurtleBot3 GUI with Velocity & Trajectory")

        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                color: #F0F0F0;
                font-family: 'Segoe UI';
                font-size: 14px;
            }

            QLabel {
                color: #E0E0E0;
                font-size: 16px;
                font-weight: bold;
            }

            QPushButton {
                background-color: #1E88E5;
                border: none;
                color: white;
                padding: 10px 16px;
                border-radius: 8px;
            }

            QPushButton:hover {
                background-color: #42A5F5;
            }

            QPushButton:pressed {
                background-color: #1565C0;
            }

            QSlider::groove:horizontal {
                background: #333;
                height: 6px;
                border-radius: 3px;
            }

            QSlider::handle:horizontal {
                background: #1E88E5;
                width: 18px;
                height: 18px;
                margin: -6px 0;
                border-radius: 9px;
            }

            QSlider::handle:horizontal:hover {
                background: #42A5F5;
            }
        """)

        # -------------------------
        # 1️⃣ Label and buttons
        # -------------------------
        self.label = QLabel("Odom: x=0.0, y=0.0")

        self.button_forward = QPushButton("Forward")
        self.button_backward = QPushButton("Backward")
        self.button_left = QPushButton("Left")
        self.button_right = QPushButton("Right")
        self.button_stop = QPushButton("Stop")
        self.button_clear_traj = QPushButton("Clear Trajectory")

        # Connect buttons
        # Forward button
        self.button_forward.clicked.connect(lambda: self.node.move(abs(self.slider_linear.value()/100.0), 0.0))
        # Backward button
        self.button_backward.clicked.connect(lambda: self.node.move(-abs(self.slider_linear.value()/100.0), 0.0))
        # Left rotation
        self.button_left.clicked.connect(lambda: self.node.move(0.0, abs(self.slider_angular.value()/100.0)))
        # Right rotation
        self.button_right.clicked.connect(lambda: self.node.move(0.0, -abs(self.slider_angular.value()/100.0)))
        self.button_stop.clicked.connect(lambda: self.node.stop())
        self.button_clear_traj.clicked.connect(self.clear_trajectory)

        # -------------------------
        # 2️⃣ Sliders for linear and angular speed
        # -------------------------
        self.slider_linear = QSlider(Qt.Horizontal)
        self.slider_linear.setMinimum(0)
        self.slider_linear.setMaximum(100)
        self.slider_linear.setValue(10)
        self.slider_linear.setTickInterval(10)
        self.slider_linear.setTickPosition(QSlider.TicksBelow)

        self.slider_angular = QSlider(Qt.Horizontal)
        self.slider_angular.setMinimum(0)
        self.slider_angular.setMaximum(100)
        self.slider_angular.setValue(10)
        self.slider_angular.setTickInterval(10)
        self.slider_angular.setTickPosition(QSlider.TicksBelow)

        # -------------------------
        # Layout for buttons and sliders
        # -------------------------
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.button_left)
        h_layout.addWidget(self.button_forward)
        h_layout.addWidget(self.button_stop)
        h_layout.addWidget(self.button_backward)
        h_layout.addWidget(self.button_right)
        h_layout.addWidget(self.button_clear_traj)
        h_layout.addWidget(QLabel("Linear Speed"))
        h_layout.addWidget(self.slider_linear)
        h_layout.addWidget(QLabel("Angular Speed"))
        h_layout.addWidget(self.slider_angular)

        # Main vertical layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addLayout(h_layout)

        # -------------------------
        # 3️⃣ Velocity graph
        # -------------------------
        self.figure = Figure(figsize=(5,3))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("Robot Velocity")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Velocity (m/s / rad/s)")

        self.linear_data = deque([0]*50, maxlen=50)
        self.angular_data = deque([0]*50, maxlen=50)
        self.line_linear, = self.ax.plot(range(50), self.linear_data, label="Linear X")
        self.line_angular, = self.ax.plot(range(50), self.angular_data, label="Angular Z")
        self.ax.legend()

        # -------------------------
        # 4️⃣ Trajectory graph
        # -------------------------
        self.figure_traj = Figure(figsize=(5,5))
        self.canvas_traj = FigureCanvas(self.figure_traj)
        layout.addWidget(self.canvas_traj)

        self.ax_traj = self.figure_traj.add_subplot(111)
        self.ax_traj.set_title("Robot Trajectory")
        self.ax_traj.set_xlabel("X (m)")
        self.ax_traj.set_ylabel("Y (m)")
        self.line_traj, = self.ax_traj.plot([], [], 'b-')
        self.ax_traj.grid(True)
        self.ax_traj.set_xlim(-10, 10)
        self.ax_traj.set_ylim(-10, 10)

        # -------------------------
        # 5️⃣ Timer to update GUI
        # -------------------------
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_gui)
        self.timer.start(100)  # 10 Hz

        self.setLayout(layout)

    def update_gui(self):
        # Update odom label
        self.label.setText(f"Odom: x={self.node.x:.2f}, y={self.node.y:.2f}")

        # Velocity smoothing
        alpha = 0.2
        if not hasattr(self, 'smoothed_linear'):
            self.smoothed_linear = self.node.linear_velocity
            self.smoothed_angular = self.node.angular_velocity
        else:
            self.smoothed_linear = alpha * self.node.linear_velocity + (1-alpha) * self.smoothed_linear
            self.smoothed_angular = alpha * self.node.angular_velocity + (1-alpha) * self.smoothed_angular

        # Update velocity graph
        self.linear_data.append(self.smoothed_linear)
        self.angular_data.append(self.smoothed_angular)
        self.line_linear.set_ydata(self.linear_data)
        self.line_angular.set_ydata(self.angular_data)
        self.line_linear.set_xdata(range(len(self.linear_data)))
        self.line_angular.set_xdata(range(len(self.angular_data)))
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw()

        # Update trajectory graph
        traj = self.node.trajectory
        if traj:
            xs, ys = zip(*traj)
            self.line_traj.set_xdata(xs)
            self.line_traj.set_ydata(ys)
            self.canvas_traj.draw()

        # # Read sliders and send velocity
        # linear = self.slider_linear.value() / 100.0
        # angular = self.slider_angular.value() / 100.0
        # self.node.move(linear_x=linear, angular_z=angular)

    def clear_trajectory(self):
        self.node.trajectory = []
        self.line_traj.set_xdata([])
        self.line_traj.set_ydata([])
        self.canvas_traj.draw()

def main(args=None):
    rclpy.init(args=args)
    node = RobotGuiNode()
    app = QApplication(sys.argv)
    window = GuiWindow(node)
    window.show()

    # Timer to spin ROS node periodically
    ros_timer = QTimer()
    ros_timer.timeout.connect(lambda: rclpy.spin_once(node, timeout_sec=0))
    ros_timer.start(50)  # 20 Hz

    sys.exit(app.exec_())
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
