import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy
from rclpy.parameter import Parameter
from std_msgs.msg import Int64, Int8MultiArray
from sensor_msgs.msg import LaserScan, NavSatFix
import math
import numpy as np
from numpy.polynomial import Polynomial
from mechaship_interfaces.msg import RelHeading, Load, Goal
from mechaship_interfaces.srv import Key, ThrottlePercentage, RGBColor
import time

import pymap3d as pm
import heapq
import pygame
import numpy as np

from autonomous.graph import nodeNode, Graph
from autonomous.grid import GridWorld
from autonomous.utils import *
from autonomous.d_star_lite import *

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY1 = (145, 145, 102)
GRAY2 = (77, 77, 51)
BLUE = (0, 0, 80)

colors = {
    0: WHITE,
    1: GREEN,
    -1: GRAY1,
    -2: GRAY2
}

# This sets the WIDTH and HEIGHT of each grid location

# This sets the margin between each cell
MARGIN = 3

# Create a 2 dimensional array. A two dimensional
# array is simply a list of lists.
grid = []
for row in range(10):
    # Add an empty array that will hold each cell
    # in this row
    grid.append([])
    for column in range(10):
        grid[row].append(0)  # Append a cell

# Set row 1, cell 5 to one. (Remember rows and
# column numbers start at zero.)
grid[1][5] = 1

# Initialize pygame
pygame.init()

X_DIM = 100
Y_DIM = 100
VIEWING_RANGE = 30

# Set title of screen
pygame.display.set_caption("D* Lite Path Planning")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock() 

# Set the HEIGHT and WIDTH of the screen

class Autonomous(Node):
    def __init__(self):
        global X_DIM, Y_DIM
        self.graph = GridWorld(X_DIM, Y_DIM)
        self.obstacle = []
        self.path = []
        
        self.first_gps = (-1,-1)
        self.s_start = ''
        self.goal_gps = []
        # self.s_goals = ['x41y70','x29y70','x29y45','x41y4',self.s_start]
        self.s_goals = ['x4y24','x4y4']
        self.s_goal = ''
        self.init_state = False
        super().__init__(
            "autonomous",
            allow_undeclared_parameters=True,
            automatically_declare_parameters_from_overrides=True,
        )        
        qos_profile = QoSProfile(
            reliability=QoSReliabilityPolicy.RMW_QOS_POLICY_RELIABILITY_BEST_EFFORT,
            history=QoSHistoryPolicy.RMW_QOS_POLICY_HISTORY_KEEP_LAST,
            depth=1,
        )
        # PNU Coordinate.
       # self.stadium_gps = [(35.23230278, 129.079367),(35.2321907, 129.0792946),(35.2321735,129.0793515), (35.2322822, 129.0794191)]
        self.stadium_gps = [(35.0696588, 128.5788018),(35.0693591, 128.5789238), (35.0693874, 129.57902290), (35.0696865, 128.57890280)]
        #self.stadium_gps = [(35.0695989, 128.5786773),(35.0692921,128.578877),(35.0693113, 128.5789217),(35.0696177, 128.5787222)]
        self.stadium_enu = [[4, 4]]
        self.angle = -10000
        for value in self.stadium_gps[1:]:
            e, n, _ = pm.geodetic2enu(value[0], value[1], 0, self.stadium_gps[0][0], self.stadium_gps[0][1], 0)
            if self.angle == -10000:
                self.angle = math.atan2(n,e)
            e, n = self.get_xy(e, n, self.angle)
            self.stadium_enu.append([n, e])
        print("stadium enu values : ", end=' ')
        print(self.stadium_enu)
        
        for value in self.goal_gps:
            e, n, _ = pm.geodetic2enu(value[0], value[1], 0, self.stadium_gps[0][0], self.stadium_gps[0][1], 0)
            e, n = self.get_xy(e, n, self.angle)
            self.s_goals.append("x"+str(n)+"y"+str(e))
    
        self.now_position = ""
        # subscriber 선언
        self.gps_subscription = self.create_subscription(NavSatFix, "/fix", self.gps_listener_callback, qos_profile)
        self.yaw_subcription = self.create_subscription(RelHeading, "/rel_yaw", self.heading_listener_callback, qos_profile)
        
        self.led_service = self.create_client(RGBColor, "/rgbled/set")
        self.scan_subscription = self.create_subscription(LaserScan, "/scan", self.listener_callback, qos_profile)
        self.queue_publish = self.create_publisher(Load, "load", qos_profile)
        #self.image_detect = self.create_subscription(Goal, "goal", self.image_detect_callback, qos_profile)
        self.msg_queue = Load()

    # ----------------------------- listner callback ---------------------------- #
    
    def heading_listener_callback(self, data):
        # Heading -> [pitch, roll, yaw]
        self.now_heading = data.rel_yaw
        self.now_heading_rad = -self.now_heading * math.pi / 180

    def listener_callback(self, data):
        if self.init_state == False:
            return
        global X_DIM, Y_DIM
        # # Go through each element and replace with row (width of grid)
       # for i in range(X_DIM):
       #     for j in range(Y_DIM):
       #         if self.graph.cells[i][j] == -1:
       #             self.graph.cells[i][j] = 0
            
      #  self.obstacle = []
        #---------------------------------------------------#
        self.angle = data.self.angle_min - self.now_heading_rad
        angle = data.angle_min
        rel_x, rel_y, abs_x, abs_y = 0, 0, 0, 0
        
        for scan_data in data.ranges:
            angle += data.angle_increment
            if  (scan_data != 0) and (not math.isinf(scan_data)) and (scan_data <= 10):
                rel_x = -scan_data*math.cos(-angle)/GRID_INTERVAL
                rel_y = -scan_data*math.sin(-angle)/GRID_INTERVAL
                print("len :" + str(scan_data) + ", angle: " + str(angle)+ ", rel_x : " + str(rel_x) + ", rel_y : " + str(rel_y))
                now_position_enu = stateNameToCoords(self.now_position)
                abs_float_x = rel_x*math.cos(self.now_heading_rad) + rel_y*math.sin(self.now_heading_rad) + now_position_enu[0]
                abs_float_y = -rel_x*math.sin(self.now_heading_rad) + rel_y*math.cos(self.now_heading_rad) + now_position_enu[1]
                abs_x = int(np.floor(abs_float_x))
                abs_y = int(np.floor(abs_float_y))
                print(abs_x, abs_y
                if (0 <= abs_x < 76 and 0 <= abs_y < 76) and (abs_x != now_position_enu[0] or abs_y != now_position_enu[1]):
                and ((abs_float_x - abs_x) > 0.5 or (abs_float_x - abs_y > 0.5))):
                    self.obstacle.append([abs_x, abs_y])
                    #self.obstacle.append([abs_x + 1, abs_y])
                    #self.obstacle.append([abs_x, abs_y + 1])
                    #self.obstacle.append([abs_x - 1, abs_y])
                    #self.obstacle.append([abs_x, abs_y - 1])
                    # 대각선
                    # self.obstacle.append([abs_x + 1, abs_y + 1])
                    # self.obstacle.append([abs_x + 1, abs_y - 1])
                    # self.obstacle.append([abs_x - 1, abs_y + 1])
                    # self.obstacle.append([abs_x - 1, abs_y - 1])
       # self.dstarlite()
            
        
    def image_detect_callback(self, data):
        if len(self.goal_coords) != 3:
            return
        else:
            if data == 1:
               now_enu= stateNameTocoords(self.now_position)
              self.graph[now_enu[1]-4][0] = -1
            elif data == 2:
                pass
            elif data == 3:
                pass
        
    def get_xy(self, e, n,angle):
        x = e * math.cos(angle) + n * math.sin(angle) + self.stadium_enu[0][1]
        y = -e * math.sin(angle) + n * math.cos(angle) + self.stadium_enu[0][0]
        return x,y
        
    def gps_listener_callback(self, data):
        self.now_gps = (data.latitude, data.longitude)
        #self.now_gps = (35.2322266999725, 129.0793471249975)
        now_e, now_n, _ = pm.geodetic2enu(self.now_gps[0], self.now_gps[1], 0, self.stadium_gps[0][0], self.stadium_gps[0][1], 0)
        now_e, now_n = self.get_xy(now_e, now_n, self.angle)
        now_enu = [now_n, now_e]
            ### 회전변환 코드 짜서 직사각형 좌표계 만들기~
        self.e_index = (int(np.floor(now_e*2)))
        self.n_index = (int(np.floor(now_n*2)))
        if self.first_gps == (-1,-1):
            self.first_gps = (self.n_index, self.e_index)
        self.msg_queue.curr_x = self.n_index
        self.msg_queue.curr_y = self.e_index
        
        self.now_position = "x"+ str(self.n_index) + "y" + str(self.e_index)
        # self.now_position = "x30y30"
        print(self.now_position)
        if self.init_state == False:
            self.init_function()
            self.init_state = True
        self.dstarlite()
    # --------------------------------------------------------------------------- #
    
    def init_function(self):
        led_color = RGBColor.Request()
        led_color.red = 255
        led_color.green = 255
        self.led_service.call_async(led_color)
        global VIEWING_RANGE

        #for i in range(75):
            #self.obstacle.append((4,i))
            #self.obstacle.append((28,i))
            # self.obstacle.append((2,i))
            # self.obstacle.append((72,i))
        self.s_start = "x" + str(self.first_gps[0]) + "y" + str(self.first_gps[1])
        self.s_goal = self.s_goals[0]
        self.graph.goal = self.s_goal
        self.goal_coords = stateNameToCoords(self.s_goal)
        self.graph.goal_coords = self.goal_coords
        self.graph.setStart(self.s_start)
        self.graph.setGoal(self.s_goal)
        self.k_m = 0
        self.s_last = self.s_start
        self.queue = []
        self.s_current = self.s_start
        self.pos_coords = stateNameToCoords(self.s_current)
        self.graph.pos_coords = self.pos_coords
        self.graph, self.queue, self.k_m = initDStarLite(self.graph, self.queue, self.s_start, self.s_goal, self.k_m)
        for item in self.obstacle:
            self.graph.cells[item[1]][item[0]] = -1
        print(self.obstacle)
        self.path, self.s_new, self.k_m = moveAndRescan(self.graph, self.queue, self.s_current, VIEWING_RANGE, self.k_m)
        print(self.path)
        self.msg_queue.list_load = self.path
        self.queue_publish.publish(self.msg_queue)


    def dstarlite(self):
        global X_DIM, Y_DIM, done
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # Change the x/y screen coordinates to grid coordinates
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)
                # Set that location to one
                if(self.graph.cells[row][column] in [0,2,3]):
                    print(row, column)
                    print("obstacle's coordinate! : " + str(column) +", " + str(row))
                    self.obstacle.append((column,row))

        if self.s_current != self.now_position:
            self.path, self.s_new, self.k_m = moveAndRescan(self.graph, self.queue, self.s_current, VIEWING_RANGE, self.k_m)
            self.msg_queue.list_load = self.path
            self.queue_publish.publish(self.msg_queue)
            
        if self.s_new == 'goal':
            goal_in_time = time.time()
            print('Goal Reached!')
            del self.s_goals[0]
            self.s_goal = self.s_goals[0]
            self.graph = GridWorld(X_DIM, Y_DIM)
            # for item in self.obstacle:
            self.goal_coords = stateNameToCoords(self.s_goal)
            self.graph.goal_coords = self.goal_coords
            self.graph.setStart(self.s_current)
            self.graph.setGoal(self.s_goal)

            led_color = RGBColor.Request()
            led_color.red = 255
            led_color.green = 255
            led_color.blue = 255
            self.led_service.call_async(led_color)

            if len(self.s_goals) == 0:
            #     self.graph.cells[item[0]][item[1]] = -1
                done = True
            self.k_m = 0
            self.queue = []
            self.pos_coords = stateNameToCoords(self.s_current)
            self.graph.pos_coords = self.pos_coords
            self.graph, self.queue, self.k_m = initDStarLite(self.graph, self.queue, self.s_current, self.s_goal, self.k_m)
            while(time.time() - goal_in_time < 3):
                print(time.time() - goal_in_time)
                pass
        else:
            led_color = RGBColor.Request()
            led_color.red = 255
            led_color.green = 255
            self.led_service.call_async(led_color)
            # print('setting s_current to ', s_new)
            for item in self.obstacle:
                self.graph.cells[item[1]][item[0]] = -1
            self.s_current = self.now_position
            self.pos_coords = stateNameToCoords(self.s_current)
            self.graph.pos_coords = self.pos_coords
            # print('got pos coords: ', pos_coords)
        render_all(self.graph)


def main(args=None):
    basicfont = pygame.font.SysFont('Comic Sans MS', 12)
    rclpy.init(args=args)
    node = Autonomous()
    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        node.get_logger().info("Keyboard Interrupt (SIGINT)")

    finally:
        node.destroy_node()
        rclpy.shutdown()
        pygame.quit()


if __name__ == "__main__":
    main()
