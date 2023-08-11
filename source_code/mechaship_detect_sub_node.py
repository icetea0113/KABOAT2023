import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data, QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy
from sensor_msgs.msg import NavSatFix, Imu
from rclpy.parameter import Parameter
from mechaship_interfaces.msg import Goal


class MechashipDetectSub(Node):
    def __init__(self):
        super().__init__(
            "Detect_sub",
            allow_undeclared_parameters=True,
            automatically_declare_parameters_from_overrides=True,
        )
        self.get_logger().info("----- goal publish -----")

        qos_profile = QoSProfile(
            reliability=QoSReliabilityPolicy.RMW_QOS_POLICY_RELIABILITY_BEST_EFFORT,
            history=QoSHistoryPolicy.RMW_QOS_POLICY_HISTORY_KEEP_LAST,
            depth=1,
        )
        # self.subscription1 = self.create_subscription(NavSatFix, "fix", self.gps_listener_callback, qos_profile)
        self.now_heading_sub = self.create_subscription(Imu, '/imu/data', self.heading_sub, qos_profile)
        

        self.now_heading_sub
       # self.subscription1
        self.set_left = ['GS','GC','RP']
        self.set_center = ['OP','RT','OC']
        self.set_right = ['OT','BP','BS']
        self.target = 'BS'
        self.goal = 0
        self.target_goal = self.create_publisher(Goal, 'goal', qos_profile)

    # def gps_listener_callback(self):
    #     if self.target in self.set_left:
    #         self.goal = 1
    #     elif self.target in self.set_center:
    #         self.goal = 2
    #     elif self.target in self.set_right:
    #         self.goal = 3
    #     goal = Goal()
    #     goal.goal = self.goal
    #     self.target_goal.publish(goal)

    def heading_sub(self, data):
        if self.target in self.set_left:
            self.goal = 1
        elif self.target in self.set_center:
            self.goal = 2
        elif self.target in self.set_right:
            self.goal = 3
        goal = Goal()
        goal.goal = self.goal
        self.target_goal.publish(goal)
        print(self.goal)
        
def main(args=None):
    rclpy.init(args=args)
    node = MechashipDetectSub()
    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        node.get_logger().info("Keyboard Interrupt (SIGINT)")

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
