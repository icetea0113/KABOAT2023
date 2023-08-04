import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy, qos_profile_sensor_data
from rclpy.parameter import Parameter
from sensor_msgs.msg import NavSatFix
import math
from std_msgs.msg import Float32
from simple_pid import PID
import pymap3d as pm
import time
import matplotlib.pyplot as plt
from mechaship_interfaces.msg import  Heading
from mechaship_interfaces.srv import Key, ThrottlePercentage, RGBColor, ThrottlePulseWidth
#from filterpy.kalman import KalmanFilter

class MotorControlNode(Node):
    def __init__(self):
        super().__init__(
            "pid_go_service",
            allow_undeclared_parameters=True,
            automatically_declare_parameters_from_overrides=True,
        )
        self.get_logger().info("----- start Hoping node -----")
        qos_profile = QoSProfile(
            reliability=QoSReliabilityPolicy.RMW_QOS_POLICY_RELIABILITY_BEST_EFFORT,
            history=QoSHistoryPolicy.RMW_QOS_POLICY_HISTORY_KEEP_LAST,
            depth=1,
        )

        self.subscription1 = self.create_subscription(NavSatFix, "fix", self.gps_listener_callback, qos_profile)
        self.subscription1
        
        self.subscription2 = self.create_subscription(Heading, "heading", self.heading_listener_callback, qos_profile)
        self.subscription2   
        
        #self.subscription3 = self.create_subscription( ~, "~", self.node_listener_callback, qos_profile)
        #self.subscription3

        
        
        self.set_throttle_handler_left = self.create_client(
            ThrottlePulseWidth, "/actuators/throttle/set_pulse_width_left"
        )
        
        self.set_throttle_handler_right = self.create_client(
            ThrottlePulseWidth, "/actuators/throttle/set_pulse_width_right"
        )

        self.origin = [35.2318379999, 129.0825561, 0]
        self.right_end= [35.2319094,129.0825094,0]
        self.right_end_x, self.right_end_y = self.gps_enu_converter(self.right_end)
        self.angle = math.atan2(self.right_end_y,self.right_end_x) #radianv

             
        
        self.motor_pid = PID(700.0/3, 0, 0)# 1.5m를 기준으로 350설계, D항은 실험을 통해 0으로 시작하여 점차 늘리며 거리별로 계산해둔다.
        self.motor_pid.output_limits = (-100, 350) # 출력 범위 제한
        self.current_position = None
        self.target_position = 6.0 # 수정
        
        self.angle_pid = PID(5.0/9, 0, 0.05)# 180기준 100
        self.angle_pid.output_limits = (-500, 500) # 출력 범위 제한(임의)
        self.current_angle = None
        self.target_angle = None  

        self.pid_status = 3 # 0 : 목표지정, 1: 각도 pid, 2: 거리 pid

        self.now_heading = 0.0
        #pid 시작할 때 방향과 갯수
        self.num = 0
        self.go = 1
        self.before_go = 1
        #pid 시작할 때 현재 노드
        self.curr_x = None # 노드값이 4라면 4부터 5까지 중간은 4.5
        self.curr_y = None
        self.diff = None
        
        self.last_time = time.time()
        
        #후진모드
        self.huzin_mode = 0
        
    # 큐에서 방향 꺽일 때를 기준으로 목표 이동 거리 및 방향 선택
 
    # 직진 할 때 거리 제어
    def pid_distance(self,y,x):

        current_time = time.time()
        dt = current_time - self.last_time
                
        self.motor_pid.setpoint = self.target_position           
        motor_speed = self.motor_pid(self.current_position,dt)
        self.last_time = current_time
            # motor_speed의 비율로 양 모터 같은 출력 나오게 채택
            # 같은 출력은 수조에서 실험후 기입
            
        if(self.huzin_mode==1):
            motor_speed *= -1 # 역추진 어떻게 하는지 보고 수정하기
        
        self.go_straight(motor_speed)
        
        if(abs(self.current_position-self.target_position)<0.1):# error 정의하기
            self.pid_status=0
            self.before_go = self.go
            self.current_position = None
            self.huzin_mode = 0
            
            #pid 다 썼으면 초기화 해두기
            self.motor_pid = PID(30, 0, 0.05)# 3.3m를 기준으로 설계
            self.motor_pid.output_limits = (0, 100)
            self.angle_pid = PID(1.0/3, 0, 0.05)# 3.3m를 기준으로 설계
            self.angle_pid.output_limits = (0, 60) # 출력 범위 제한(임의)                    
           

    #누적 오차로 예상 이외의 점으로 가는거 괜찮나? # 오차도 어느 범위 왔을 때 멈출지랑 들어왔을 때 조금 그 값으로 수렴하게 시간을 더 줄 수도 있다.
    
    def heading_listener_callback(self, data):
        self.now_heading = data.yaw

    def gps_listener_callback(self, gps):

        e, n= self.gps_enu_converter([gps.latitude, gps.longitude, gps.altitude])
        y, x = self.get_xy(e,n)
        self.current_position = y


        fig, ax = plt.subplots()
        ax.plot(y, x, 'o')  # 'o' for dot-like markers, you can change to '-' for line
        ax.set_xlabel('Y')
        ax.set_ylabel('X')
        ax.set_title('GPS Data in Local Coordinate')
        ax.grid(True)
        ax.set_xlim([0, 10])
        ax.set_ylim([0, 20])
        ax.text(x, y, f'({x}, {y})')

        plt.show()

        if(self.pid_status ==2):
            self.pid_distance(y,x)

    def gps_enu_converter(self,gnss):
        e, n, u = pm.geodetic2enu(gnss[0], gnss[1], gnss[2], self.origin[0], self.origin[1], self.origin[2])
        return e, n
    
    def get_xy(self,e,n):
        angle = self.angle
        x = e * math.cos(angle) + n * math.sin(angle)
        y = -e * math.sin(angle) + n * math.cos(angle)
        return x, y
    
    def angle_difference(a, b):
        diff = (b - a + 180) % 360 - 180
        return diff
    
    def go_straight(self,percentage):# 음수로 역회전을 하는건가?
        throttle = ThrottlePulseWidth.Request()
        left_percentage= percentage + 1500
        right_percentage= percentage + 1500
        
        throttle.pulse_width = int(left_percentage)
        self.set_throttle_handler_left.call_async(throttle)
        
        throttle.pulse_width = int(right_percentage)
        self.set_throttle_handler_right.call_async(throttle)

       
    
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