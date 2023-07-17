import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy
from rclpy.parameter import Parameter
from sensor_msgs.msg import NavSatFix
import math
import pymap3d as pm
import numpy as np
#import time
#from mechaship_interfaces.msg import Classification, ClassificationArray, Heading, DetectionArray
#from mechaship_interfaces.srv import Key, ThrottlePercentage, RGBColor, ThrottlePulseWidth
#from filterpy.kalman import KalmanFilter

class Hopping(Node):
    def __init__(self):
        super().__init__(
            "gps_xy_location",
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
        self.origin = [35.2324897999, 129.0794665, 114.173]
        self.right_end= [35.2324608,129.0794053,0]

        self.right_end_x, self.right_end_y = self.gps_enu_converter(self.right_end)
        self.angle = math.atan2(self.right_end_y,self.right_end_x) #radian
   
        self.now_gps = [0.0,0.0]

        self.area_arr = np.zeros[3600,55]# revise go
        self.area_gps = [0,0]
        
        self.window =[]
                
    def gps_listener_callback(self, gps):
        #self.get_logger().info('gps data: "%s"' % gps)
        
        e, n= self.gps_enu_converter([gps.latitude, gps.longitude, gps.altitude])
        x, y = self.get_xy(e,n)
        
        
        #using moving_average_filter
        #x_filtered = self.moving_average_filter(x,5)
        #y_filtered = self.moving_average_filter(y,5)
        #self.area_gps[0]= round(x_filtered*10)
        #self.area_gps[1] = round(y_filtered*10)
        
        #self.now_gps[0] = x
        #self.now_gps[1] = y
        self.area_gps[0]= round(x*10)
        self.area_gps[1] = round(y*10)
                
        print(self.area_gps)
        #print("now :",self.now_gps[0], "," , self.now_gps[1])
    
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
        window = []
    
        if len(window) < window_size:
            window.append(data)
            return 0.0
        else:
            window.pop(0)
            window.append(data)
        
            #filtered_data.append(sum(window) / len(window))
        return sum(window)/len(window)
    
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
