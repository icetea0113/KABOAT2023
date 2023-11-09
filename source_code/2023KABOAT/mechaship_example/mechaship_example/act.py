import rclpy
from rclpy.node import Node
from mechaship_interfaces.srv import Key, ThrottlePulseWidth, ThrottlePercentage

class Actuator(Node):
    def __init__(self):
        super().__init__(
                "Actuator",
                allow_undeclared_parameters=True,
                automatically_declare_parameters_from_overrides=True,
            )

        self.set_throttle_handler_left = self.create_client(
            ThrottlePulseWidth, "/actuators/throttle/set_pulse_width_left"
        )
        
        self.set_throttle_handler_right = self.create_client(
            ThrottlePulseWidth, "/actuators/throttle/set_pulse_width_right"
        )
        self.stop()
        
    def stop(self):
        throttle = ThrottlePulseWidth.Request()
        throttle.pulse_width = 1500
        print(throttle)
        for _ in range(2):
            self.set_throttle_handler_left.call_async(throttle)
            self.set_throttle_handler_right.call_async(throttle)

def main(args=None):
    rclpy.init(args=args)
    node = Actuator()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
