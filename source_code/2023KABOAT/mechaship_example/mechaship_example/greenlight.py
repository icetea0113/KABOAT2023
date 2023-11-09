import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from rclpy.parameter import Parameter
from mechaship_interfaces.srv import RGBColor

class Greenlight(Node):
    def __init__(self):
        super().__init__(
            "greenlight_node",
            allow_undeclared_parameters=True,
            automatically_declare_parameters_from_overrides=True,
        )
        self.set_color_handler = self.create_client(RGBColor, "rgbled/set")
        self.light()

    def light(self):
        color = RGBColor.Request()
        color.red = 0
        color.green = 255
        color.blue = 0
        self.set_color_handler.call_async(color)

def main(args=None):
    rclpy.init(args=args)
    node = Greenlight()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
