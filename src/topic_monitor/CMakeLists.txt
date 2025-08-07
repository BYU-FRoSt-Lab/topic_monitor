cmake_minimum_required(VERSION 3.8 FATAL_ERROR)
project(frost_topic_monitor CXX)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(ament_index_cpp REQUIRED)
find_package(rosidl_runtime_cpp REQUIRED)
find_package(rosidl_typesupport_introspection_cpp REQUIRED)
find_package(yaml-cpp REQUIRED)

# ADD THIS: Explicitly find and link rclcpp_serialization
# find_package(rclcpp_serialization REQUIRED)


# Define the executable
add_executable(frost_topic_monitor_node src/frost_topic_monitor_node.cpp)

# Link necessary libraries
ament_target_dependencies(frost_topic_monitor_node
  rclcpp
  std_msgs
  sensor_msgs
  nav_msgs
  ament_index_cpp
  rosidl_runtime_cpp
  rosidl_typesupport_introspection_cpp
)

target_link_libraries(frost_topic_monitor_node yaml-cpp)

# Install the executable
install(TARGETS
  frost_topic_monitor_node
  DESTINATION lib/${PROJECT_NAME}
)

# Install the topics.txt file to the package's share directory
install(FILES topics.yaml
  DESTINATION share/${PROJECT_NAME}
)

ament_export_dependencies(
  rclcpp
  std_msgs
  sensor_msgs
  nav_msgs
  ament_index_cpp
  rosidl_runtime_cpp
  rosidl_typesupport_introspection_cpp
  rclcpp_serialization # ADD THIS
)

ament_package()