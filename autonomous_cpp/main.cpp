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
#include "mechaship_interfaces/msg/heading.hpp"

#define GRID_INTERVAL 0.5
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
int map_total[22][72] = {0, }; //autodriving map 36m*11m*0.5m | interval : 50cm(0.5m)
int map_tournament[13][80] = {0, }; //tournament map 40m*6.5m*0.5m | interval : 50cm(0.5m)
double rel_x, rel_y; // Relative coordinates are inevitably declared as double to minimize errors while displaying in absolute coordinates.
int abs_x, abs_y;
int now_position_x=10, now_position_y =30;
double now_heading;
double now_heading_rad;
queue<pair<double, double>> waypoints_gps;
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
           heading_subscriber_ = this->create_subscription<mechaship_interfaces::msg::Heading>(
            "/heading", default_qos, std::bind(&Sub::head_callback, this, _1));

            cout << "now_position : " << now_position_x << ", " << now_position_y << endl;
            map_total[now_position_x][now_position_y] = 5;
            subscription_ = this->create_subscription<sensor_msgs::msg::LaserScan>(
              "/scan", default_qos, std::bind(&Sub::topic_callback, this, _1));
        }
        double angle_increment;
        void head_callback(const mechaship_interfaces::msg::Heading::SharedPtr msg){
          now_heading = msg->yaw;
          now_heading_rad = now_heading * M_PI / 180;
        }

    private:
        void topic_callback(const sensor_msgs::msg::LaserScan::SharedPtr msg){
        // Initialize the map to be all zeros at the start of each scan
        memset(map_total, 0, sizeof(map_total));

        double angle_increment = msg->angle_increment;

        for(long unsigned int i=0; i<msg->ranges.size(); i++){
            double angle = msg->angle_min + i * angle_increment - now_heading_rad;

            rel_x = msg->ranges[i]*cos(angle)/GRID_INTERVAL;
            rel_y = msg->ranges[i]*sin(angle)/GRID_INTERVAL;

            abs_x = round(now_position_x + rel_x);
            abs_y = round(now_position_y + rel_y);

            // Check if the absolute coordinates are within the map
            if (abs_x >= 0 && abs_x < 22 && abs_y >= 0 && abs_y < 72) {
                // Mark the obstacle on the map
                if (msg->ranges[i] != INT_MAX && msg->ranges[i] != 0){
                    map_total[abs_x][abs_y] = 1;
                }
            }
        }
        // create visual console map using LiDAR
        
        cout << "**************************" << endl;
        for(int i=0; i<22; i++){
          for(int j=0; j<72; j++){
            if(map_total[i][j] == 0)  cout << ".";
            else cout << map_total[i][j];
          }
          cout << endl;
        }
        cout << "**************************" << endl;
        
        /* Step 4. Select coordinate and control motor(ESC signal)*/
        /* TO DO: Set the front() of the Queue as the destination so that it can move towards that place.
          If there are several coordinates with the same distance (when the size of the vector is not one), select the case where the y-axis goes ahead.




        */


        /* always. Checks the current location and synchronizes it with the map coordinates so that it moves appropriately to the map coordinates. */
      }
      rclcpp::Subscription<mechaship_interfaces::msg::Heading>::SharedPtr heading_subscriber_;
      rclcpp::Subscription<sensor_msgs::msg::LaserScan>::SharedPtr subscription_;
      sensor_msgs::msg::LaserScan::SharedPtr laser1_;
};

int main(int argc, char **argv) {
  rclcpp::init(argc, argv);

  auto node = std::make_shared<Sub>();

  rclcpp::spin(node);

  rclcpp::shutdown();


  return 0;
}