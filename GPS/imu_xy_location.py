"""Subscribe IMU Magnetometer data and calculate boat's heading direction
Notes:
    Heading: -180 (to West) ~ 180 (to East) (deg), Magnetic North is 0 deg
"""
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy
from sensor_msgs.msg import Imu
from std_msgs.msg import Float64
import time
import math
import numpy as np
#from filterpy.kalman import KalmanFilter
#from mechaship_interfaces.msg import Classification, ClassificationArray, DetectionArray,Heading

class HeadingAngle(Node):
    
    def __init__(self):
        super().__init__("imu_xy_location")

        qos_profile = QoSProfile(
            reliability=QoSReliabilityPolicy.RMW_QOS_POLICY_RELIABILITY_BEST_EFFORT,
            history=QoSHistoryPolicy.RMW_QOS_POLICY_HISTORY_KEEP_LAST,
            depth=1,
        )
        self.subscription = self.create_subscription(Float64, "heading/final", self.heading_angle_callback, qos_profile)
        self.subscription  # prevent unused variable warning
        self.subscription2 = self.create_subscription(Imu, "imu/data_raw", self.imu_callback, qos_profile)
        self.subscription2  # prevent unused variable warning
        
        self.heading_publisher = self.create_publisher(Float64, 'heading2', qos_profile)
        
        #self.now_heading_subscription = self.create_subscription(
        #    Heading, "heading", self.heading_listener_callback, qos_profile
        #)
        #self.now_heading_subscription = self.create_subscription(
        #    Float64, "heading1", self.heading_listener_call, qos_profile
        #)
        
        self.acc_x = 0.0
        self.acc_y = 0.0 
        
        self.acc_x_dif = 0.0
        self.acc_y_dif = 0.0
        self.acc_z_dif = 0.0
        
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.distance_x = 0.0
        self.distance_y = 0.0
        self.before_acc_x = 0.0
        self.before_acc_y = 0.0
        self.before_vel_x = 0.0
        self.before_vel_y = 0.0
        
        self.total_distance_x = 0.0
        self.total_distance_y = 0.0
        
        self.t =0.0 # temporal
        
        
        #self.get_logger().info("start_ init")
        
        self.i = 0
        
        self.time_now = 0.0
        self.time_before = 0.0
        
        self.ang_diff = 0.0
        
        self.roll = 0.0
        self.pitch = 0.0
        self.yaw = 0.0
        self.p = 0
        self.sum_x = 0.0
        self.sum_y = 0.0
        
        
        self.step = 0
        
        
        
    def heading_angle_callback(self, data):
        # Heading -> [pitch, roll, yaw]  
        self.roll = math.radians(data.roll)
        self.pitch = math.radians(data.pitch)
        self.yaw = data.yaw
        
    #def heading_listener_call(self, data):
    #    self.yaw = data.data
          
        
    def imu_callback(self, imu):
        
        if(self.p<100):
            self.sum_x += imu.linear_acceleration.x
            self.sum_y += imu.linear_acceleration.y
        elif(self.p == 100):
            self.acc_x_dif = self.sum_x/100.0
            self.acc_y_dif = self.sum_y/100.0
        else: 
            self.time_now = time.time()        
            self.acc_x = -(imu.linear_acceleration.x - self.acc_x_dif) - 9.81 * math.sin(self.pitch)
            self.acc_y = -(imu.linear_acceleration.y - self.acc_y_dif + 9.81 * math.cos(self.roll))
            self.t = self.time_now-self.time_before
            self.acc_cal()
        
            print(self.total_distance_x,"  ", self.total_distance_y)
            self.time_before = self.time_now
        self.p +=1
        

    #def heading_angle_callback(self, heading_angle):
    #    self.last_heading_angle = heading_angle.data
        

    def acc_cal(self):

        #angle = self.yaw*math.pi/180
        #sin_angle = math.sin(angle)
        #cos_angle = math.cos(angle)
        #x_acc = self.acc_y * sin_angle + self.acc_x * cos_angle
        #y_acc = self.acc_y * cos_angle - self.acc_x * sin_angle
        
        if(self.i > 0):
            self.vel_x = self.vel_x + (self.before_acc_x + self.acc_x ) * 0.5 * self.t
            self.vel_y = self.vel_y + (self.before_acc_y + self.acc_y ) * 0.5 * self.t
        
            self.distance_x = self.distance_x + (self.before_vel_x + self.vel_x ) * 0.5 * self.t
            self.distance_y = self.distance_y + (self.before_vel_y + self.vel_y ) * 0.5 * self.t
            
            if(self.step==0):
                self.total_distance_x = self.total_distance_x + self.distance_x
            else:
                self.total_distance_y = self.total_distance_y + self.distance_x
            
            #self.total_distance_y = self.total_distance_y + self.distance_y

        self.i += 1
        self.before_acc_x = self.acc_x
        self.before_acc_y = self.acc_y
        self.before_vel_x = self.vel_x
        self.before_vel_y = self.vel_y
    
    '''def kalman_gps_imu(self): #plus average filtering good
        a = [0.0,0.0]
        b1= [0.0,0.0]
        x = np.array([a[0]],[a[1]],[0],[0])
        b = np.array([b[0]],[b[1]])
        dt = 1
        F = np.array([[1,0,dt,0],
                      [0,1,0,dt],
                      [0,0,1,0],
                      [0,0,0,1]])
        P = np.eye(4)*100
        Q = np.array([[0.01,0,0,0],
                      [0,0.01,0,0],
                      [0,0,0.01,0],
                      [0,0,0,0.01]])
        H = np.array([[1,0,0,0],
                      [0,1,0,0]])
        
        R = np.array([[0.1,0]
                      [0,0.1]])
        
        kf = KalmanFilter(initial_state_mean=x.ravel(), initial_state_covariance=P, 
                  transition_matrices=F, observation_matrices=H, 
                  observation_covariance=R, transition_covariance=Q)
        for i in range(len(a)):
        # 예측 단계
            x_pred, P_pred = kf.predict()

    # 추정 단계
            #y = b[i] - H @ x_pred  # 이전 예측과 새로운 측정 값 차이 계산
            x_est, P_est, K = kf.update(b[i], H)  # 칼만 게인 계산 및 새로운 예측 값 계산

    # 결과 출력
        print("Estimated position: ", x_est[0], x_est[1])'''
        
def main(args=None):
    
    rclpy.init(args=args)
    heading = HeadingAngle()
    rclpy.spin(heading)
    
    #heading.heading_publisher.publish(angle)
    heading.destroy_node()
    rclpy.shutdown()
    #rate = rospy.Rate(10)  # 10 Hz


    '''while not rospy.is_shutdown():
        heading_angle = heading.calculate_heading_angle()
        heading.pub.publish(round(heading_angle, 2))
        
        rate.sleep()'''


if __name__ == "__main__":
    main()
