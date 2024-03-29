import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from rclpy.qos import qos_profile_sensor_data

from ls2n_interfaces.msg import KeepAlive

qos_profile_sensor_data.depth = 1


class MinimalPublisher(Node):
    def __init__(self):
        super().__init__("minimal_publisher")
        self.get_logger().info("Minimal Publisher Node Created")
        self.declare_parameter("no_drone", "1")
        self.declare_parameter("position", [2.0, 2.0, 1.0, 0.0])
        my_param = self.get_parameter("no_drone").get_parameter_value().string_value
        posi = self.get_parameter("position").get_parameter_value().double_array_value
        drone: str = "Drone" + my_param

        self.joint_msg = JointTrajectory()
        self.joint_msg.joint_names = ["x", "y", "z", "yaw"]

        posi[1] = posi[1] + float(my_param) - 1

        self.joint_point = JointTrajectoryPoint()
        self.joint_point.positions = posi

        self.joint_msg.points = [self.joint_point]
        self.traj_pub = self.create_publisher(
            JointTrajectory, f"/{drone}/Trajectory", qos_profile_sensor_data
        )
        self.create_timer(0.05, self.publish_trajectory)

    def publish_trajectory(self) -> None:
        self.joint_msg.header.stamp = self.get_clock().now().to_msg()
        self.traj_pub.publish(self.joint_msg)
        self.get_logger().info("Published Trajectory")


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
