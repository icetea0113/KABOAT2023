import rclpy
from rclpy.node import Node
from mechaship_interfaces.srv import Key, ThrottlePulseWidth, ThrottlePercentage
#from filterpy.kalman import KalmanFilter


class Actuator(Node):
    def __init__(self):
        super().__init__(
                "pid_go",
                allow_undeclared_parameters=True,
                automatically_declare_parameters_from_overrides=True,
            )

        self.set_throttle_handler_left = self.create_client(
            ThrottlePulseWidth, "/actuators/throttle/set_pulse_width_left"
        )
        self.set_throttle_handler_right = self.create_client(
            ThrottlePercentage, "/actuators/throttle/set_percentage_right"
        )
        throttle_percent = ThrottlePercentage.Request()
        throttle_percent.percentage = 0
        throttle_pulse_width = ThrottlePulseWidth.Request()
        throttle_pulse_width.pulse_width = 1500
        self.set_throttle_handler_left(throttle_pulse_width)
        self.set_throttle_handler_right(throttle_percent)

def main(args=None):
    rclpy.init(args=args)
    node = Actuator()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()