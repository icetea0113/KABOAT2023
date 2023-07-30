import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data, QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge
from mechaship_interfaces.msg import DetectionArray, Goal


class MechashipDetectSub(Node):
    def __init__(self):
        super().__init__("mechaship_detect_sub_node")

        self.image_subscription = self.create_subscription(
            Image, "/Image", self.image_listener_callback, qos_profile_sensor_data
        )
        self.detection_subscription = self.create_subscription(
            DetectionArray,
            "/DetectionArray",
            self.detection_listener_callback,
            qos_profile_sensor_data,
        )
        qos_profile = QoSProfile(
            reliability=QoSReliabilityPolicy.RMW_QOS_POLICY_RELIABILITY_BEST_EFFORT,
            history=QoSHistoryPolicy.RMW_QOS_POLICY_HISTORY_KEEP_LAST,
            depth=1,
        )
        self.target_goal = self.create_publisher(Goal, 'goal', qos_profile)
        self.image_subscription  # prevent unused variable warning
        self.detection_subscription  # prevent unused variable warning

        self.br = CvBridge()
        self.detections = DetectionArray().detections
        self.set_left = ['BC','RC','GC']
        self.set_center = ['BT','RT','GT']
        self.set_right = ['BS','RS','GS']
        self.target = ['RT']
        self.goal = 0

    def detection_listener_callback(self, data):
        self.get_logger().info("detection cnt: %s" % (len(data.detections)))
        self.detections = data.detections

    def image_listener_callback(self, data):
        right = False
        center = False
        left = False
        origin_image = self.br.imgmsg_to_cv2(data, "bgr8")
        if origin_image.all() == None or len(origin_image) == 0:
            return
        if len(self.detections) != 0:
            for detection in self.detections:
                if (detection.name in self.set_right):
                    right = True
                    if detection.name in self.target:
                        print("target in right")
                        self.goal = 3
                    else:
                        if right == True and center == False and left == False:
                            pass
                        #more turn code in here
                elif (detection.name in self.set_center):
                    center = True
                    right = True
                    if detection.name in self.target:
                        self.goal = 2
                        print("target in center")
                    else:
                        if right == True and center == True and left == False:
                            self.goal = 1
                elif (detection.name in self.set_left):
                    left = True
                    center = True
                    right = True
                    if detection.name in self.target:
                        self.goal = 1
                        print("target in left")
                else:
                    print("target not in screen")
                    #more turn code in here

                cv2.rectangle(
                    origin_image,
                    (int(detection.xmin), int(detection.ymin)),
                    (int(detection.xmax), int(detection.ymax)),
                    (0, 0, 255),
                    3,
                )
        cv2.imshow("detected image", origin_image)
        cv2.waitKey(1)
        goal = Goal()
        goal.goal = self.goal
        self.target_goal.publish(goal)


def main(args=None):
    rclpy.init(args=args)
    node = MechashipDetectSub()
    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        node.get_logger().info("Keyboard Interrupt (SIGINT)")

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
