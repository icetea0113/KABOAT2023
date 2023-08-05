import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy
from mechaship_interfaces.msg import Heading
from mechaship_interfaces.msg import RelHeading
from mechaship_interfaces.msg import StartHeading
import numpy as np

class RelativeYawNode(Node):

    def __init__(self):
        super().__init__('RelativeYaw_node')
        qos_profile = QoSProfile(
            reliability=QoSReliabilityPolicy.RMW_QOS_POLICY_RELIABILITY_BEST_EFFORT,
            history=QoSHistoryPolicy.RMW_QOS_POLICY_HISTORY_KEEP_LAST,
            depth=1,
        )
        self.yaw_values = []
        self.avg_yaw = None
        self.now_heading = self.create_subscription(Heading, '/heading', self.imu_callback, qos_profile)
        self.relative_heading = self.create_publisher(RelHeading, '/rel_yaw', qos_profile)
        # self.start_heading = self.create_publisher(StartHeading, '/start_heading', qos_profile)
        self.timer = self.create_timer(10.0, self.timer_callback)  # add a timer callback

        self.get_logger().info('Relative heading node initialized') 
        self.yaw_z = 10000  # 값을 정상적으로 계산하는지 확인하기 위해 초기값을 10000으로 설정

    def imu_callback(self, msg):
        yaw = msg.yaw
        if self.avg_yaw is None:
            self.yaw_values.append(yaw)
        else:
            relative_yaw = yaw - self.avg_yaw

            if relative_yaw > 180:
                relative_yaw -= 360
            elif relative_yaw < -180:
                relative_yaw += 360

            self.get_logger().info(f"Relative yaw: {relative_yaw}")
            msg = RelHeading()
            msg.rel_yaw = relative_yaw
            self.relative_heading.publish(msg)
            
            # start = StartHeading()
            # start.st_yaw = self.avg_yaw
            # self.start_heading.publish(start)

    def timer_callback(self):
        if self.avg_yaw is None and len(self.yaw_values) > 0:
            self.avg_yaw = np.mean(self.yaw_values)
            self.get_logger().info(f"Average yaw calculated: {self.avg_yaw}")
            self.timer.cancel()  # stop the timer after calculating the average

    
def main(args=None):
    rclpy.init(args=args)
    yaw_calculator = RelativeYawNode()
    rclpy.spin(yaw_calculator)
    yaw_calculator.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
