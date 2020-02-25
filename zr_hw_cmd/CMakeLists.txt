cmake_minimum_required(VERSION 2.8.3)
project(zr_hw_cmd)


find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs

)
include_directories(
  ${catkin_INCLUDE_DIRS}
)

catkin_python_setup()



