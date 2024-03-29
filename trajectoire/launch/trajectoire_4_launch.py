from launch import LaunchDescription
from launch_ros.actions import Node
from simple_launch import SimpleLauncher


def generate_launch_description():
    sl = SimpleLauncher()
    sl.declare_arg(
        "pos", default_value=[2.0, 2.0, 1.0, 0.0], description="position du drone 1"
    )
    for i in range(4):
        with sl.group(if_condition=True):
            sl.node(
                "trajectoire",
                "trajectoire",
                parameters={"no_drone": str(i + 1), "position": sl.arg("pos")},
            )
    return sl.launch_description()
