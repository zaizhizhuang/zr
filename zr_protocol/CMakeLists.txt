cmake_minimum_required(VERSION 2.8.3)
project(zr_protocol)
find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
)
find_package(catkin REQUIRED COMPONENTS
  message_generation
)
add_message_files(DIRECTORY msg FILES
  led8_data8.msg
  screen_1602.msg
  bit8_data.msg
)
add_service_files(DIRECTORY srv FILES
  hw_info.srv
  hw_cmd.srv
)
generate_messages(DEPENDENCIES std_msgs)

