#include <stdbool.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>

#include <Arduino.h>
#include <HardwareSerial.h>

#include <micro_ros_platformio.h>

#include <rcl/rcl.h>
#include <rclc/executor.h>
#include <rclc/rclc.h>

#include <rmw_microros/rmw_microros.h>

// topic message
#include <sensor_msgs/msg/imu.h>
#include <sensor_msgs/msg/joint_state.h>
#include <sensor_msgs/msg/magnetic_field.h>
#include <sensor_msgs/msg/nav_sat_fix.h>
#include <std_msgs/msg/bool.h>

// service message
#include <mechaship_interfaces/srv/battery.h>
#include <mechaship_interfaces/srv/key.h>
#include <mechaship_interfaces/srv/rgb_color.h>
#include <mechaship_interfaces/srv/throttle_percentage.h>
#include <mechaship_interfaces/srv/throttle_pulse_width.h>
#include <std_srvs/srv/trigger.h>

#include "bsp/bsp.h"
#include "modules/include/modules.h"

#include "hw.h"
#include "supporter.h"

static HardwareSerial *s_serial;

static rcl_allocator_t s_allocator;
static rclc_support_t s_support;
static rclc_executor_t s_executor;

static rcl_node_t s_node;

// static rcl_timer_t s_gy87_timer_h;
// static rcl_timer_t s_gps_timer_get_h;
// static rcl_timer_t s_gps_timer_send_h;
// static rcl_timer_t s_joint_state_timer_send_h;

// static rcl_publisher_t s_gy87_publisher_imu_h;        // gy87 imu(자이로+가속도)
// static rcl_publisher_t s_gy87_publisher_mag_h;        // gy87 지자기
// static rcl_publisher_t s_gps_publisher_h;             // gps
// static rcl_publisher_t s_joint_state_publisher_key_h; // 키 joint state
static rcl_publisher_t s_emo_publisher_h;             // EMO

static std_msgs__msg__Bool s_emo_msg;

// static rcl_service_t s_gy87_service_offset_calibration_h;
// static std_srvs__srv__Trigger_Request s_gy87_service_offset_calibration_req;
// static std_srvs__srv__Trigger_Response s_gy87_service_offset_calibration_res;

static rcl_service_t s_battery_service_get_data_h;
static mechaship_interfaces__srv__Battery_Request s_battery_service_get_data_req;
static mechaship_interfaces__srv__Battery_Response s_battery_service_get_data_res;

static rcl_service_t s_throttle_service_set_percentage_left_h;
static mechaship_interfaces__srv__ThrottlePercentage_Request s_throttle_service_set_percentage_left_req;
static mechaship_interfaces__srv__ThrottlePercentage_Response s_throttle_service_set_percentage_left_res;

static rcl_service_t s_throttle_service_set_pulse_width_left_h;
static mechaship_interfaces__srv__ThrottlePulseWidth_Request s_throttle_service_set_pulse_width_left_req;
static mechaship_interfaces__srv__ThrottlePulseWidth_Response s_throttle_service_set_pulse_width_left_res;

static rcl_service_t s_throttle_service_set_percentage_right_h;
static mechaship_interfaces__srv__ThrottlePercentage_Request s_throttle_service_set_percentage_right_req;
static mechaship_interfaces__srv__ThrottlePercentage_Response s_throttle_service_set_percentage_right_res;

static rcl_service_t s_throttle_service_set_pulse_width_right_h;
static mechaship_interfaces__srv__ThrottlePulseWidth_Request s_throttle_service_set_pulse_width_right_req;
static mechaship_interfaces__srv__ThrottlePulseWidth_Response s_throttle_service_set_pulse_width_right_res;

// static rcl_service_t s_key_service_set_h;
// static mechaship_interfaces__srv__Key_Request s_key_service_set_req;
// static mechaship_interfaces__srv__Key_Response s_key_service_set_res;

static rcl_service_t s_rgb_service_set_h;
static mechaship_interfaces__srv__RGBColor_Request s_rgb_service_set_req;
static mechaship_interfaces__srv__RGBColor_Response s_rgb_service_set_res;

bsp_throttle_handle_t throttle_left_h;
bsp_throttle_handle_t throttle_right_h;
// bsp_key_handle_t key_h;
bsp_neopixel_handler_t neopixel_h;

UART Serial2(8, 9, NC, NC);

typedef enum {
  WAITING_AGENT,
  AGENT_AVAILABLE,
  AGENT_CONNECTED,
  AGENT_DISCONNECTED
} state_t;
static state_t s_state;

static bool s_create_entities(void) {
  s_allocator = rcl_get_default_allocator();
  RCCHECK(rclc_support_init(&s_support, 0, NULL, &s_allocator));

  size_t executor_cnt = 0;

  s_node = rcl_get_zero_initialized_node();
  rcl_node_options_t node_ops = rcl_node_get_default_options();
  node_ops.domain_id = HW_CFG_ROS_DOMAIN_ID;
  RCCHECK(rclc_node_init_with_options(&s_node, "mechaship_mcu_driver", "", &s_support, &node_ops));

  // EMO publisher
  RCCHECK(rclc_publisher_init_default(&s_emo_publisher_h, &s_node,
                                      ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Bool), "emo_event"));

  // battery service
  RCCHECK(rclc_service_init_default(&s_battery_service_get_data_h, &s_node,
                                    ROSIDL_GET_SRV_TYPE_SUPPORT(mechaship_interfaces, srv, Battery), "battery/get_data"));
  executor_cnt++;

  // throttle service
  RCCHECK(rclc_service_init_default(&s_throttle_service_set_percentage_left_h, &s_node,
                                    ROSIDL_GET_SRV_TYPE_SUPPORT(mechaship_interfaces, srv, ThrottlePercentage), "actuators/throttle/set_percentage_left"));
  executor_cnt++;
  RCCHECK(rclc_service_init_default(&s_throttle_service_set_pulse_width_left_h, &s_node,
                                    ROSIDL_GET_SRV_TYPE_SUPPORT(mechaship_interfaces, srv, ThrottlePulseWidth), "actuators/throttle/set_pulse_width_left"));
  executor_cnt++;
  
  RCCHECK(rclc_service_init_default(&s_throttle_service_set_percentage_right_h, &s_node,
                                    ROSIDL_GET_SRV_TYPE_SUPPORT(mechaship_interfaces, srv, ThrottlePercentage), "actuators/throttle/set_percentage_right"));
  executor_cnt++;
  RCCHECK(rclc_service_init_default(&s_throttle_service_set_pulse_width_right_h, &s_node,
                                    ROSIDL_GET_SRV_TYPE_SUPPORT(mechaship_interfaces, srv, ThrottlePulseWidth), "actuators/throttle/set_pulse_width_right"));
  executor_cnt++;

  // rgb color service
  RCCHECK(rclc_service_init_default(&s_rgb_service_set_h, &s_node,
                                    ROSIDL_GET_SRV_TYPE_SUPPORT(mechaship_interfaces, srv, RGBColor), "rgbled/set"));
  executor_cnt++;

  // excutor
  RCCHECK(rclc_executor_init(&s_executor, &s_support.context, executor_cnt, &s_allocator));

  RCCHECK(rclc_executor_add_service(&s_executor, &s_battery_service_get_data_h,
                                    &s_battery_service_get_data_req, &s_battery_service_get_data_res,
                                    battery_service_get_data_callback));
                                    
  RCCHECK(rclc_executor_add_service(&s_executor, &s_throttle_service_set_percentage_left_h,
                                    &s_throttle_service_set_percentage_left_req, &s_throttle_service_set_percentage_left_res,
                                    left_throttle_service_set_percentage_callback));
  RCCHECK(rclc_executor_add_service(&s_executor, &s_throttle_service_set_pulse_width_left_h,
                                    &s_throttle_service_set_pulse_width_left_req, &s_throttle_service_set_pulse_width_left_res,
                                    left_throttle_service_set_pulse_width_callback));

  RCCHECK(rclc_executor_add_service(&s_executor, &s_throttle_service_set_percentage_right_h,
                                    &s_throttle_service_set_percentage_right_req, &s_throttle_service_set_percentage_right_res,
                                    right_throttle_service_set_percentage_callback));
  RCCHECK(rclc_executor_add_service(&s_executor, &s_throttle_service_set_pulse_width_right_h,
                                    &s_throttle_service_set_pulse_width_right_req, &s_throttle_service_set_pulse_width_right_res,
                                    right_throttle_service_set_pulse_width_callback));

  RCCHECK(rclc_executor_add_service(&s_executor, &s_rgb_service_set_h,
                                    &s_rgb_service_set_req, &s_rgb_service_set_res,
                                    rgb_service_set_callback));

  return true;
}

static void s_destroy_entities(void) {
  rmw_context_t *rmw_context = rcl_context_get_rmw_context(&s_support.context);
  (void)rmw_uros_set_context_entity_destroy_session_timeout(rmw_context, 0);

  // EMO publisher
  RCCHECK(rcl_publisher_fini(&s_emo_publisher_h, &s_node));

  // battery service
  RCCHECK(rcl_service_fini(&s_battery_service_get_data_h, &s_node));

  // throttle service
  RCCHECK(rcl_service_fini(&s_throttle_service_set_percentage_left_h, &s_node));
  RCCHECK(rcl_service_fini(&s_throttle_service_set_pulse_width_left_h, &s_node));

  RCCHECK(rcl_service_fini(&s_throttle_service_set_percentage_right_h, &s_node));
  RCCHECK(rcl_service_fini(&s_throttle_service_set_pulse_width_right_h, &s_node));

  // rgb color service
  RCCHECK(rcl_service_fini(&s_rgb_service_set_h, &s_node));

  rclc_executor_fini(&s_executor);
  RCCHECK(rcl_node_fini(&s_node));
  rclc_support_fini(&s_support);
}

static void s_monitor_status() {
  bool is_emo = digitalRead(HW_PIN_EMO);
  bool is_agent = s_state == AGENT_CONNECTED;

  static bool is_emo_last = false;
  static bool is_agent_last = true;
  static unsigned long nxt_blink_time = 0;
  static bool toggle = false;
  if (is_emo != is_emo_last || is_agent != is_agent_last) {
    if (is_emo == true && is_emo != is_emo_last) {
      HW_SERIAL_DEBUG.println("[\"s_monitor_status\"]EMO Pressed!");
      bsp_throttle_set_emo(&throttle_left_h);
      bsp_throttle_set_emo(&throttle_right_h);
      s_emo_msg.data = true;
      rcl_publish(&s_emo_publisher_h, &s_emo_msg, NULL);
    } else if (is_emo != is_emo_last) {
      HW_SERIAL_DEBUG.println("[\"s_monitor_status\"]EMO Released!");
      bsp_throttle_reset_emo(&throttle_left_h);
      bsp_throttle_reset_emo(&throttle_right_h);
      bsp_neopixel_set(&neopixel_h, 0, 0, 0, 0);
      digitalWrite(HW_PIN_STATUS_LED, HIGH);
      s_emo_msg.data = false;
      rcl_publish(&s_emo_publisher_h, &s_emo_msg, NULL);
    }
    if (is_agent == true && is_agent != is_agent_last) {
      HW_SERIAL_DEBUG.println("[\"s_monitor_status\"]Agent Connected!");
      bsp_neopixel_set(&neopixel_h, 0, 0, 0, 0);
      digitalWrite(HW_PIN_STATUS_LED, HIGH);
    } else if (is_agent != is_agent_last) {
      HW_SERIAL_DEBUG.println("[\"s_monitor_status\"]Agent Disconnected!");
    }
    nxt_blink_time = 0;
    toggle = false;
    is_emo_last = is_emo;
    is_agent_last = is_agent;
  }

  if (nxt_blink_time <= millis()) {
    if (is_emo == true) {
      bsp_neopixel_set(&neopixel_h, ((toggle = !toggle) == true) ? 255 : 0, 0, 0, 0);
      digitalWrite(HW_PIN_STATUS_LED, (toggle == true) ? HIGH : LOW);
      nxt_blink_time = millis() + 500;
      return;
    }
    if (is_agent == false) {
      bsp_neopixel_set(&neopixel_h, ((toggle = !toggle) == true) ? 255 : 0, (toggle == true) ? 100 : 0, 0, 0);
      digitalWrite(HW_PIN_STATUS_LED, (toggle == true) ? HIGH : LOW);
      nxt_blink_time = millis() + 1000;
      return;
    }
  }
  return;
}

void setup() {
  digitalWrite(HW_PIN_RESET, HIGH);

  HW_SERIAL_DEBUG.begin(115200);

  // neopixel init
  neopixel_h.pin_num = HW_PIN_NEOPIXEL;
  neopixel_h.pixel_cnt = HW_CFG_NEOPIXEL_PIXEL_CNT;
  bsp_neopixel_init(&neopixel_h);
  bsp_neopixel_set(&neopixel_h, 255, 100, 0, 0);

  // microros serial init
  HW_SERIAL_MICROROS.begin(115200);
  set_microros_serial_transports(HW_SERIAL_MICROROS);

  // battery init
  bsp_battery_conf_t battery_conf = {
      .pin_adc = HW_PIN_BATTERY,
      .pin_20p_led = HW_PIN_BATTERY_20P_LED,
      .pin_40p_led = HW_PIN_BATTERY_40P_LED,
      .pin_60p_led = HW_PIN_BATTERY_60P_LED,
      .pin_80p_led = HW_PIN_BATTERY_80P_LED,
      .adc_resolution = 12,
      .adc_voltage_max = 3.3,
      .max_voltage = 2.1,
      .min_voltage = 0,
  };
  ERRCHECK(bsp_battery_init(&battery_conf));

  // throttle init
  throttle_right_h.pin_num = HW_PIN_THROTTLE_RIGHT;
  throttle_right_h.min_pwr_pulse_width = 1500;
  throttle_right_h.max_pwr_pulse_width = 2000;
  bsp_throttle_init(&throttle_right_h);
  bsp_throttle_set_by_percentage(&throttle_right_h, 0);

  throttle_left_h.pin_num = HW_PIN_THROTTLE_LEFT;
  throttle_left_h.min_pwr_pulse_width = 1500;
  throttle_left_h.max_pwr_pulse_width = 2000;
  bsp_throttle_init(&throttle_left_h);
  bsp_throttle_set_by_percentage(&throttle_left_h, 0);

  pinMode(HW_PIN_STATUS_LED, OUTPUT);
  digitalWrite(HW_PIN_STATUS_LED, LOW);
  pinMode(HW_PIN_EMO, INPUT_PULLUP);

  s_state = WAITING_AGENT;

  bsp_neopixel_set(&neopixel_h, 0, 0, 0, 0);
}

void loop() {
  switch (s_state) {
  case WAITING_AGENT:
    EXECUTE_EVERY_N_MS(500, s_state = (RMW_RET_OK == rmw_uros_ping_agent(100, 1)) ? AGENT_AVAILABLE : WAITING_AGENT;);
    break;
  case AGENT_AVAILABLE:
    s_state = (true == s_create_entities()) ? AGENT_CONNECTED : WAITING_AGENT;
    if (s_state == WAITING_AGENT) {
      s_destroy_entities();
    };
    break;
  case AGENT_CONNECTED:
    EXECUTE_EVERY_N_MS(200, s_state = (RMW_RET_OK == rmw_uros_ping_agent(100, 1)) ? AGENT_CONNECTED : AGENT_DISCONNECTED;);
    if (s_state == AGENT_CONNECTED) {
      rclc_executor_spin_some(&s_executor, RCL_MS_TO_NS(100));
    }
    break;
  case AGENT_DISCONNECTED:
    s_destroy_entities();
    s_state = WAITING_AGENT;
    break;
  default:
    break;
  }

  s_monitor_status();

  EXECUTE_EVERY_N_MS(1000, bsp_battery_update_led());
}