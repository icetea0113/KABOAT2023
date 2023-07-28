import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy, qos_profile_sensor_data
from rclpy.parameter import Parameter
from sensor_msgs.msg import NavSatFix
import math
from std_msgs.msg import Float32
from simple_pid import PID
import pymap3d as pm
#import numpy as np
#from queue import Queue
#import time
#from mechaship_interfaces.msg import  Heading
#from mechaship_interfaces.srv import Key, ThrottlePercentage, RGBColor, ThrottlePulseWidth
#from filterpy.kalman import KalmanFilter

class MotorControlNode(Node):
    def __init__(self):
        super().__init__(
            "pid_go",
            allow_undeclared_parameters=True,
            automatically_declare_parameters_from_overrides=True,
        )
        self.get_logger().info("----- start Hoping node -----")
        qos_profile = QoSProfile(
            reliability=QoSReliabilityPolicy.RMW_QOS_POLICY_RELIABILITY_BEST_EFFORT,
            history=QoSHistoryPolicy.RMW_QOS_POLICY_HISTORY_KEEP_LAST,
            depth=1,
        )

        self.subscription = self.create_subscription(NavSatFix, "fix", self.gps_listener_callback, qos_profile)
        self.subscription
        
        self.motor_pid = PID(30, 0, 0.05)# 3.3m를 기준으로 설계
        self.motor_pid.output_limits = (0, 100) # 출력 범위 제한
        self.current_position = None
        self.target_position = None
        
        self.angle_pid = PID(1.0/3, 0, 0.05)# 3.3m를 기준으로 설계
        self.motor_pid.output_limits = (0, 60) # 출력 범위 제한(임의)
        self.current_anlge = None
        self.target_angle = None        
 
 
    # 직진 할 때 거리 제어
    def pid_distance(self):
        if self.target_position is not None and self.current_position is not None:
            self.motor_pid.setpoint = self.target_position
            error = self.target_position - self.current_position
            motor_speed = self.motor_pid(error)
            # motor_speed의 비율로 양 모터 같은 출력 나오게 채택
            # 같은 출력은 수조에서 실험후 기입
    # 방향 틀 때 각도 제어        
    def pid_angle(self):
        #시계방향으로 돌릴지 반시계방향으로 돌릴지 판단 코드
        #시작 각도와 목표 각도 잡고 pid 제어
        #모터를 반대 방향으로 같은 크기로 돌리는데 그 크기를 각도 오차를 통해서 pid 제어
        #이때는 비례상수가 최대 차이 180도 일 때 임의의 같은 출력(ex 60출력) -> 비례상수 1/3수준으로 지정
        
        pass
    
    def gps_listener_callback(self, gps):
        #self.get_logger().info('gps data: "%s"' % gps)
        e, n= self.gps_enu_converter([gps.latitude, gps.longitude, gps.altitude])
        x, y = self.get_xy(e,n)    
    
    def gps_enu_converter(self,gnss):
        e, n, u = pm.geodetic2enu(gnss[0], gnss[1], gnss[2], self.origin[0], self.origin[1], self.origin[2])
        return e, n
    
    def get_xy(self,e,n):
        angle = self.angle
        x = e * math.cos(angle) + n * math.sin(angle)
        y = -e * math.sin(angle) + n * math.cos(angle)
        return x, y
        
       
    
def main(args=None):
    rclpy.init(args=args)
    node = MotorControlNode()
    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        node.get_logger().info("Keyboard Interrupt (SIGINT)")

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
#yaw 0도 만들어주는거
#gps : #반올림 해서 하는게 맞을지, 배열에 1 올렸다가 지울지, 여유 범위를 어느정도로 할지 (40으로 하고 싶다. - 안되는 case 생각해보자)그냥 반올림만 해도 될거 같은데 
#다음 index로 가는 go code와 도착했다는 기준(출발하면서 목표 index를 정해둬야함. self로)

#go_goal 코드(throttle )

#다 막혔다 했을 때 --> 다시 값 받게
#경기장 밖(음의값 index 가지는) -->if문으로 해결