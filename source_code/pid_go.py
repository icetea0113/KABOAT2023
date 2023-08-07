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
from mechaship_interfaces.msg import  RelHeading
from mechaship_interfaces.srv import Key, ThrottlePercentage, RGBColor, ThrottlePulseWidth
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

        self.subscription1 = self.create_subscription(NavSatFix, "fix", self.gps_listener_callback, qos_profile)
        self.subscription1
        
        self.subscription2 = self.create_subscription(RelHeading, "/rel_yaw", self.heading_listener_callback, qos_profile)
        self.subscription2   
        
        #self.subscription3 = self.create_subscription( ~, "~", self.node_listener_callback, qos_profile)
        #self.subscription3

        
        
        self.set_throttle_handler_left = self.create_client(
            ThrottlePulseWidth, "/actuators/throttle/set_pulse_width_left"
        )
        
        self.set_throttle_handler_right = self.create_client(
            ThrottlePulseWidth, "/actuators/throttle/set_pulse_width_right"
        )

        self.origin =[35.2323084,129.0792833,0]
        self.right_end=  [35.232304, 129.0792801, 0]
        self.right_end_x, self.right_end_y = self.gps_enu_converter(self.right_end)
        self.angle = math.atan2(self.right_end_y,self.right_end_x) #radianv

             
        
        self.motor_pid = PID(700.0/3, 0, 0)# 1.5m를 기준으로 350설계, D항은 실험을 통해 0으로 시작하여 점차 늘리며 거리별로 계산해둔다.
        self.motor_pid.output_limits = (-100, 350) # 출력 범위 제한
        self.current_position = None
        self.target_position = 4.0 # 수정
        self.window = []
        
        self.angle_pid = PID(10.0/9, 0, 0.05)# 180기준 200
        self.angle_pid.output_limits = (-200, 200) # 출력 범위 제한(임의)
        self.current_angle = None
        self.target_angle = 90.0  

        self.go_pid = PID(2,0,0) #10도에 20 정도 더 주는 정도
        self.go_pid.output_limits = (-100, 100)
  

        self.pid_status = 4 # 0 : 목표지정, 1: 각도 pid, 2: 거리 pid

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
        
        #if(abs(self.current_position-self.target_position)<0.1):# error 정의하기
        #    self.pid_status=0
        #    self.before_go = self.go
        #    self.current_position = None
        #    self.huzin_mode = 0
            
        #    #pid 다 썼으면 초기화 해두기
        #    self.motor_pid = PID(30, 0, 0.05)# 3.3m를 기준으로 설계
        #    self.motor_pid.output_limits = (0, 100)
        #    self.angle_pid = PID(1.0/3, 0, 0.05)# 3.3m를 기준으로 설계
        #    self.angle_pid.output_limits = (0, 60) # 출력 범위 제한(임의)
                                
    def pid_angle(self):
        #시계방향으로 돌릴지 반시계방향으로 돌릴지 판단 코드
        #시작 각도와 목표 각도 잡고 pid 제어
        #모터를 반대 방향으로 같은 크기로 돌리는데 그 크기를 각도 오차를 통해서 pid 제어
        #이때는 비례상수가 최대 차이 180도 일 때 임의의 같은 출력(ex 60출력) -> 비례상수 1/3수준으로 지정


        error = self.angle_difference(self.target_angle,self.now_heading)      
        self.angle_pid.setpoint = 0
        
        current_time = time.time()
        dt = current_time - self.last_time
           
        #error가 양수이면 시계방향 회전, 음수이면 반시계방향 회전                
        motor_speed = self.angle_pid(error, dt)
        self.last_time = current_time
        
        self.turn_angle(motor_speed,1)
        
        #if(error>0):
        #    self.turn_angle(motor_speed,1)
        #else:
        #    self.turn_anlge(motor_speed,2)
            
        #if(error<3.0):# error 정의하기
        #    self.pid_status=2
            #1초나 2초 기다리는 코드 추가할까?       

    #누적 오차로 예상 이외의 점으로 가는거 괜찮나? # 오차도 어느 범위 왔을 때 멈출지랑 들어왔을 때 조금 그 값으로 수렴하게 시간을 더 줄 수도 있다.
    
    def heading_listener_callback(self, data):
        self.now_heading = round(data.rel_yaw,2)
        
        if(self.pid_status == 1):               
            self.pid_angle()
        if(self.pid_status == 3):               
            self.go_temp()                
        print(self.now_heading)
       # print(self.pid_status)
    def gps_listener_callback(self, gps):

        e, n= self.gps_enu_converter([gps.latitude, gps.longitude, gps.altitude])
        y, x = self.get_xy(e,n)
        self.current_position = y

        data_filtered = self.moving_average_filter([y,x],3)
        y_dot= data_filtered[0]
        x_dot = data_filtered[1]
        #print("x_filtered : ",x_dot,"  y_filtered : ",y_dot)
        print("x : ",x,"  y : ",y) 


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
    
    def angle_difference(self,a, b):
        diff = (b - a + 180) % 360 - 180
        return diff

    def go_temp(self):
        
        error = self.angle_difference(self.target_angle,self.now_heading)    
        self.go_pid.setpoint = 0
        motor_speed = self.go_pid(error)
        
        throttle = ThrottlePulseWidth.Request()
        throttle.pulse_width = 1650
        
        self.set_throttle_handler_left.call_async(throttle)
        
        self.set_throttle_handler_right.call_async(throttle)
        throttle.pulse_width = 1650 + int(motor_speed)
    
    def go_straight(self,percentage):
        throttle = ThrottlePulseWidth.Request()
        if percentage < 80 and percentage>50:
            percentage =80
        if (percentage < -50) and (percentage >-80):
            percentage = -80
        if 50 > percentage > -50: # 50을 내는게 한 21cm정도 오차 pid_status 변화시키지 않으면 그 안에서 조정 된다.
            percentage = 0
            self.pid_status = 4 # 연습할 때 pid _status 1으로 두고 90꺽는거 보기 그리고  다시 status 3으로 바꿔서 90도 일치 시키면서 도는거 
        left_percentage= percentage + 1500
        right_percentage= percentage + 1500
        
        throttle.pulse_width = int(left_percentage)
        self.set_throttle_handler_left.call_async(throttle)
        
        throttle.pulse_width = int(right_percentage)
        self.set_throttle_handler_right.call_async(throttle)

    def turn_angle(self,percentage,direction):
        throttle = ThrottlePulseWidth.Request()
        if percentage < 80 and percentage>30:
            percentage =80
        if (percentage < -30) and (percentage >-80):
            percentage = -80
        if 30 > percentage > -30:
            percentage = 0
            throttle.pulse_width = 1500
            self.set_throttle_handler_left.call_async(throttle)
            self.set_throttle_handler_right.call_async(throttle)
            self.pid_status = 3
            return
        #print(percentage)
        left_pulse_width = percentage*-1
        right_pulse_width = percentage 
        
        #if(direction == 2):
        #    left_pulse_width *= -1            
        #    right_pulse_width *= -1
        #print("left",left_pulse_width,"right",right_pulse_width)
        left_pulse_width += 1500
        right_pulse_width +=1500
        print(left_pulse_width, right_pulse_width)
        throttle.pulse_width = int(left_pulse_width)
        self.set_throttle_handler_left.call_async(throttle)
        
        throttle.pulse_width = int(right_pulse_width)
        self.set_throttle_handler_right.call_async(throttle)
    
    def moving_average_filter(self,data,window_size):
        #filtered_data = []
    
        if len(self.window) < window_size:
            self.window.append(data)
            return [0.0] * len(data)
        else:
            self.window.pop(0)
            self.window.append(data)
                    
        filtered_data = [sum(col) / len(col) for col in zip(*self.window)]
        return filtered_data
        
    def stop_motors(self):
        # 모터를 정지시키는 코드
        throttle = ThrottlePulseWidth.Request()
        throttle.pulse_width = 0
        self.set_throttle_handler_left.call_async(throttle)
        self.set_throttle_handler_right.call_async(throttle)

    def destroy_node(self):
        self.stop_motors()  # 모터 정지 메서드 호출
        super().destroy_node()       
    
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
