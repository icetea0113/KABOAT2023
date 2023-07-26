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

class Location(Node):
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
        self.origin = [35.2318379999, 129.0825561, 0.0]
        self.right_end= [35.2319094,129.0825094,0.0]

        self.right_end_x, self.right_end_y = self.gps_enu_converter(self.right_end)
        self.angle = math.atan2(self.right_end_y,self.right_end_x) #radian
   
        self.now_gps = [0.0,0.0]

        #self.area_arr = np.zeros[3600,55]# revise go
        self.area_gps = [0,0]
        
        self.window =[]
                
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
    
def main(args=None):
    rclpy.init(args=args)
    node = Location()
    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        node.get_logger().info("Keyboard Interrupt (SIGINT)")

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
