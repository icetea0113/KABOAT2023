#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/laser_scan.hpp"
#include <cmath>
#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
#include <string>
#include <memory>
#include <functional>
#include <chrono>
#include <climits>

#define GRID_INTERVAL 0.1
using std::placeholders::_1;
using namespace std::chrono_literals;
using namespace std;

/*
  *Our LiDAR Info (YDLiDAR TG30):
    1. angle increment : 0.003742 rad (0.214413 deg)
      1.1. If you need to change angle increment, you should change number of 'frequency'
          at params/ydlidar.yaml in ydlidar_ros2_driver package
    2. Min/Max degree : -180 ~ 180

  *Our Algorithm (step)W
    1. Create map. (L.H)
    2. Display waypoints on the coordinate system of the map. (U)
    3. Detect obstacle and display on the coordinate system of the map. (L.H)
    4. Select coordinate and control motor(ESC signal) (L.H)

    always 1. Checks the current location and synchronizes it with the map coordinates so that it moves appropriately to the map coordinates. (U, S)
    always 2. If you are moving to the selected coordinates, skip Step 4. (L.H, U, S)

    check point. If the coordinates of the destination pass waypoint 1, yolov5 is activated so that it can drive at an appropriate angle. (L.H, L.Y)
*/

/* Step 1. Create map */
int map_total[110][360] = {0, }; //autodriving map 36m*11m*0.5m 
int map_tournament[65][400] = {0, }; //tournament map 40m*6.5m*0.5m 
double rel_x, rel_y; // Relative coordinates are inevitably declared as double to minimize errors while displaying in absolute coordinates.
int abs_x, abs_y;
int now_position_x=30, now_position_y =50;
double now_heading;
queue<pair<double, double>> waypoints_gps; //See the loop statement in the main function.
queue<pair<int, int>> waypoints_map;

class Sub : public rclcpp::Node
{
    public:
        Sub() : Node("sub")
        {   
            auto default_qos = rclcpp::QoS(rclcpp::SensorDataQoS());
            RCLCPP_INFO(this->get_logger(), "Hello!");
            /* Step 2. Display waypoints on the coordinate system of the map. */
            /* TO DO : It should be displayed on the coordinate system of the map using the GPS coordinates of the given waypoints.
              Set the destination using Queue, and pop from the Queue when passing the destination. If you don't understand, please ask me.
            
            
            
            */
            cout << "now_position : " << now_position_x << ", " << now_position_y << endl;
            map_total[now_position_x][now_position_y] = 5;
            subscription_ = this->create_subscription<sensor_msgs::msg::LaserScan>(
              "/scan", default_qos, std::bind(&Sub::topic_callback, this, _1));
        }
        double angle_increment;

    private:
      void topic_callback(const sensor_msgs::msg::LaserScan::SharedPtr msg){
        int map_total[110][360] = {0, }; //autodriving map 36m*11m*0.5m 
        int now_position_x=30, now_position_y =50;
        map_total[now_position_x][now_position_y] = 5;

        //RCLCPP_INFO(this->get_logger(), "this angle_increment: '%f'", msg->angle_increment);
        angle_increment = msg->angle_increment;

        /*Step 3. Detect obstacle and display on the coordinate system of the map.*/
        for(long unsigned int i=0; i<msg->ranges.size(); i++){
          if (msg->ranges[i] != INT_MAX && msg->ranges[i] != 0){
            //Relative coordinates are inevitably declared as double to minimize errors while displaying in absolute coordinates.
            if (i < 359)  if (abs(msg->ranges[i] - msg->ranges[i+1]) > 0.03)  continue;
            rel_x = msg->ranges[i]*cos(i*angle_increment)/GRID_INTERVAL;
            rel_y = msg->ranges[i]*sin(i*angle_increment)/GRID_INTERVAL;
            abs_x = round(rel_x*cos(now_heading) + rel_y*sin(now_heading) + now_position_x);
            abs_y = round(-rel_x*sin(now_heading) + rel_y*cos(now_heading) + now_position_y);
            for (int j=-2; j<3; j++){
              for (int k=-2; k<3; k++){
                if(abs_x+j < 0 || abs_y+k <0 || abs_x+j >= 110 || abs_y+k >= 360) continue;
                map_total[abs_x+j][abs_y+k] = 1;
              }
            }
          }
        }
        // create visual console map using LiDAR
        cout << "**************************" << endl;
        for(int i=0; i<110; i++){
          for(int j=0; j<360; j++){
            if(map_total[i][j] == 0)  cout << ".";
            else cout << map_total[i][j];
          }
          cout << endl;
        }
        cout << "**************************" << endl;
        
        /* Step 4. Select coordinate and control motor(ESC signal)*/
        /* TO DO: Set the front() of the Queue as the destination so that it can move towards that place.
          If there are several coordinates with the same distance (when the size of the vector is not one), select the case where the y-axis goes ahead.

          if 



        */


        /* always. Checks the current location and synchronizes it with the map coordinates so that it moves appropriately to the map coordinates. */
      }
      rclcpp::Subscription<sensor_msgs::msg::LaserScan>::SharedPtr subscription_;
      sensor_msgs::msg::LaserScan::SharedPtr laser1_;
};

int main(int argc, char **argv) {

  pair<double, double> gps[4] = {make_pair(0,0),make_pair(0,0),make_pair(0,0),make_pair(0,0)};

  for (int i=0; i<4; i++) waypoints_gps.push(gps[i]);

  rclcpp::init(argc, argv);

  auto node = std::make_shared<Sub>();

  rclcpp::spin(node);

  rclcpp::shutdown();


  return 0;
}