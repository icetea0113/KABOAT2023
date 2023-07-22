import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy
from rclpy.parameter import Parameter
from sensor_msgs.msg import NavSatFix
import math
import pymap3d as pm
import numpy as np
from queue import Queue
#import time
#from mechaship_interfaces.msg import Classification, ClassificationArray, Heading, DetectionArray
#from mechaship_interfaces.srv import Key, ThrottlePercentage, RGBColor, ThrottlePulseWidth
#from filterpy.kalman import KalmanFilter

class Hopping(Node):
    def __init__(self):
        super().__init__(
            "autonomous_hopping",
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
        
        #start & square_end
        self.origin = [35.2318379999, 129.0825561, 0.0]
        self.right_end= [35.2319094,129.0825094,0.0]

        self.right_end_x, self.right_end_y = self.gps_enu_converter(self.right_end)
        self.angle = math.atan2(self.right_end_y,self.right_end_x) #radian
   
        self.now_gps = [0.0,0.0]

        self.area_arr = np.zeros((3600,55))# revise go
        
        self.window =[]
        self.goal_num = 1
        self.status_now = 1
        
        
        #goal_queue
        self.my_queue = Queue()
        self.queues =  [(2, 2), (3, 3), (3, 3)]
        for element in self.queues:
            self.my_queue.put(element)
        #  self.my_queue.get() 
        
        self.goal_location = (1,1)
        #self.goal_location = self.my_queue.get()
        
                
    def gps_listener_callback(self, gps):
        #self.get_logger().info('gps data: "%s"' % gps)
        
        e, n= self.gps_enu_converter([gps.latitude, gps.longitude, gps.altitude])
        x, y = self.get_xy(e,n)
        
        
            #using moving_average_filter
        #data_filtered = self.moving_average_filter([x,y],5)
        #x_dot= round(data_filtered[0]*10)
        #y_dot = round(data_filtered[1]*10)

        
        x_dot= round(x*10)
        y_dot = round(y*10)
        print(x_dot,"   ",y_dot)
        data = [# 1=up, 2=down, 3=left, 4=right
            (1, x_dot+1, y_dot,self.area_arr[x_dot+1,y_dot], self.euclidean_distance(x_dot+1,y_dot,self.goal_location[0],self.goal_location[1])),
            (2, x_dot-1, y_dot,self.area_arr[x_dot-1,y_dot], self.euclidean_distance(x_dot-1,y_dot,self.goal_location[0],self.goal_location[1])),
            (3, x_dot, y_dot+1,self.area_arr[x_dot,y_dot+1], self.euclidean_distance(x_dot,y_dot+1,self.goal_location[0],self.goal_location[1])),
            (4, x_dot, y_dot-1,self.area_arr[x_dot,y_dot-1], self.euclidean_distance(x_dot,y_dot-1,self.goal_location[0],self.goal_location[1]))
        ]# same value -> up,down prior
        sorted_data = sorted(data, key=lambda item: (item[3], item[4]))

        closest_value = None
        min_distance = float('inf')  

        for row in sorted_data: # prior first : row[3](first go), second : distance to goal
            if row[3] == 0:  
                closest_value = row[0]  
                break
            elif row[3] == 1:  
                # close distance select
                if row[4] < min_distance:
                    closest_value = row[0]
                    min_distance = row[4]
            else:
                # thinking~
                return 0       
        self.area_arr[x_dot,y_dot] = 1 # passed route = 1
        
        self.go_goal(closest_value)
        
        return 0
        
            # if find index == negative  - code gogo
   
        
    
    def gps_enu_converter(self,gnss):
        e, n, u = pm.geodetic2enu(gnss[0], gnss[1], gnss[2], self.origin[0], self.origin[1], self.origin[2])
        return e, n
    
    def get_xy(self,e,n):
        angle = self.angle
        x = e * math.cos(angle) + n * math.sin(angle)
        y = -e * math.sin(angle) + n * math.cos(angle)
        return x, y
    
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
    
    def go_goal(self,direction):
        # 1
        if(direction == 1):
            #yaw = 0 change go 10cm
            return 0
        elif(direction == 2):
            #yaw = 180 change go 10cm
            return 0
        elif(direction == 3):
            #yaw = 90 change go 10cm
            return 0
        elif(direction ==4):
            #yaw = -90 change go 10cm
            return 0
            
        return 0    
    
    
    def euclidean_distance(self,x1, y1, x2, y2):
        
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)         
    
     
    
def main(args=None):
    rclpy.init(args=args)
    node = Hopping()
    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        node.get_logger().info("Keyboard Interrupt (SIGINT)")

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
