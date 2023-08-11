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
#import numpy as np
#from queue import Queue
from mechaship_interfaces.msg import  RelHeading, Load
from mechaship_interfaces.srv import  ThrottlePulseWidth
#from filterpy.kalman import KalmanFilter

class MotorControlNode(Node):
    def __init__(self):
        super().__init__(
            "pid_go2",
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
        
        self.subscription3 = self.create_subscription(Load , "load", self.node_listener_callback, qos_profile)
        self.subscription3

        
        
        self.set_throttle_handler_left = self.create_client(
            ThrottlePulseWidth, "/actuators/throttle/set_pulse_width_left"
        )
        
        self.set_throttle_handler_right = self.create_client(
            ThrottlePulseWidth, "/actuators/throttle/set_pulse_width_right"
        )

        self.origin = [35.2318379999, 129.0825561, 0.0]
        self.right_end= [35.2319094,129.0825094,0.0]
        self.right_end_x, self.right_end_y = self.gps_enu_converter(self.right_end)
        self.angle = math.atan2(self.right_end_y,self.right_end_x) #radianv

        self.motor_pid = PID(200.0/3, 0,50)# 1.5m를 기준으로 100설계, D항은 실험을 통해 0으로 시작하여 점차 늘리며 거리별로 계산해둔다.
        self.motor_pid.output_limits = (-80, 200) # 출력 범위 제한
        self.current_position = None
        self.target_position = 0 # 수정
        self.window = []
        
        self.angle_pid = PID(10.0/9, 0, 0.05)# 180기준 200
        self.angle_pid.output_limits = (-200, 200) # 출력 범위 제한(임의)
        self.current_angle = None
        self.target_angle = 0

        self.go_pid = PID(4,0,3) #10도에 20 정도 더 주는 정도
        self.go_pid.output_limits = (-200, 200)
  

        self.pid_status = 0 # 0 : 목표지정, 1: 각도 pid, 2: 거리 pid 3 : 직진하면서 각도 각도 제어

        self.now_heading = 0.0
        #pid 시작할 때 방향과 갯수
        self.num = 0
        self.go = 1
        self.before_go = 2
        #pid 시작할 때 현재 노드

        # 지금은 안쓰임
        self.target_x = None 
        self.target_y = None
        self.diff = None
        
        self.last_time = time.time()
        
        #후진모드
        self.huzin_mode = 0
        
    # 큐에서 방향 꺽일 때를 기준으로 목표 이동 거리 및 방향 선택
 
    # 직진 할 때 거리 제어
    def pid_distance(self,y,x):
      
        #목표 지점 정하기 (한번만 하면 돼서, 수정해주면 좋을 거 같다), status가 0에서 1로 바뀌며 go, num 넘겨 줄 때 같이 해주면 될듯
        if(self.current_position == None):
            if(self.go == 1):
                self.target_position = math.round(x) + self.num
            elif(self.go == 2):
                self.target_position = math.round(y) + self.num
            elif(self.go == 3):
                self.target_position = math.round(x) - self.num
            elif(self.go == 4):
                self.target_position = math.round(y) - self.num
            
        if(self.go ==1 or self.go == 4):
            self.current_position = y
        else:
            self.current_position = x            
        
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
                            
           
    def pid_angle(self):

        error = self.angle_difference(self.target_angle,self.now_heading)      
        self.angle_pid.setpoint = 0
        
        current_time = time.time()
        dt = current_time - self.last_time
           
        #error가 양수이면 시계방향 회전, 음수이면 반시계방향 회전                
        motor_speed = self.angle_pid(error, dt)
        self.last_time = current_time
        
        self.turn_angle(motor_speed)
            
               
    #누적 오차로 예상 이외의 점으로 가는거 괜찮나? # 오차도 어느 범위 왔을 때 멈출지랑 들어왔을 때 조금 그 값으로 수렴하게 시간을 더 줄 수도 있다.
    
    def heading_listener_callback(self, data):
        self.now_heading = round(data.rel_yaw,2)

        if(self.pid_status == 1):
            # 후진 하는 상황인지 보고 아니면 각도 조정
            if((self.before_go==1 and self.go ==3) or (self.before_go==4 and self.go ==2) or (self.before_go==2 and self.go ==4) or (self.before_go==3 and self.go ==1)):
                if self.num < 2:    
                    self.huzin_mode = 1
                    self.pid_status = 2
            else:                
                self.pid_angle()
        
    def gps_listener_callback(self, gps):
        e, n= self.gps_enu_converter([gps.latitude, gps.longitude, gps.altitude])
        y, x = self.get_xy(e,n)# 경기장 위쪽을 y로 하겠다.

        if(self.pid_status ==2):
            self.pid_distance(y,x)
    
    def node_listener_callback(self, data):
        if(self.pid_status==0):
            i = 0
            self.num=1
            while (i < len(self.list_load) - 1 )and(self.list_load[i] == self.list_load[i+1]):
                self.go = self.list_load[i]
                self.num +=1
                i +=1

            if self.go == 1:
                self.target_angle = 90 #  정수 or 실수?
            elif self.go == 2:
                self.target_angle = 0
            elif self.go == 3:
                self.target_angle = -90
            elif self.go == 4:
                self.target_angle = 180

            self.pid_status = 1       
            self.huzin_mode = 0
            #pid 제어 초기화 넣기 

            if self.num > 12:
                self.num=12
            print("num =   ",self.num,"go :   ",self.go)
            self.motor_pid = PID(200.0/3, 0,50)# 1.5m를 기준으로 100설계, D항은 실험을 통해 0으로 시작하여 점차 늘리며 거리별로 계산해둔다.
            self.motor_pid.output_limits = (-80, 200) # 출력 범위 제한   

            self.angle_pid = PID(10.0/9, 0, 0.05)# 180기준 200
            self.angle_pid.output_limits = (-200, 200) # 출력 범위 제한(임의)

            self.go_pid = PID(4,0,2) #10도에 20 정도 더 주는 정도
            self.go_pid.output_limits = (-200, 200)         

            # 거리 멀 때랑(급정거 넣을지) 0.5m일 때 \
            
            if self.num > 11:
                self.motor_pid = PID(300.0/3, 0,70)# 1.5m를 기준으로 100설계, D항은 실험을 통해 0으로 시작하여 점차 늘리며 거리별로 계산해둔다.
                self.motor_pid.output_limits = (-80, 350)


              
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
        if percentage < 80 and percentage>70:
            percentage =80
        if 70 > percentage >30: # 50을 내는게 한 21cm정도 오차 pid_status 변화시키지 않으면 그 안에서 조정 된다.
            percentage = 0
        #if (percentage < 35) and (percentage >-80):
            #self.pid_status = 4
            #print(self.pid_status)
            #return
        if 30 >percentage> -15 : # 다음으로 넘겨주는 코드
            self.before_go = self.go
            self.pid_status = 0# pid 초기화 넣기

        if -80 < percentage < -15: # 혹시 넘기면 아니면 장거리 직진 후 way point에서 2초 할 때 급 정거
            percentage = -80   

        
        ##### 추가 시작
        error = self.angle_difference(self.target_angle,self.now_heading)    
        self.go_pid.setpoint = 0
        motor_speed = self.go_pid(error)
        
        throttle = ThrottlePulseWidth.Request()
        
        if(motor_speed>0):
            right_percentage= percentage + 1500 + motor_speed
            left_percentage= percentage + 1500 - motor_speed
        else:
            right_percentage= percentage + 1500 +motor_speed
            left_percentage= percentage + 1500 - motor_speed
        #### 추가 끝
        #print(left_percentage, right_percentage)
        
        throttle.pulse_width = int(left_percentage)
        self.set_throttle_handler_left.call_async(throttle)
        
        throttle.pulse_width = int(right_percentage)
        self.set_throttle_handler_right.call_async(throttle)
        
    def turn_angle(self,percentage):# 음수로 역회전을 하는건가?

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
            self.pid_status = 0
            return
        #print(percentage)
        left_pulse_width = percentage*-1
        right_pulse_width = percentage 
        
        left_pulse_width += 1500
        right_pulse_width +=1500
        #print(left_pulse_width, right_pulse_width)
        throttle.pulse_width = int(left_pulse_width)
        self.set_throttle_handler_left.call_async(throttle)
        
        throttle.pulse_width = int(right_pulse_width)
        self.set_throttle_handler_right.call_async(throttle)    

    def stop_motors(self):
        # 모터를 정지시키는 코드
        throttle = ThrottlePulseWidth.Request()
        throttle.pulse_width = 0
        for _ in range(2):
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