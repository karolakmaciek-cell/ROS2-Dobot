cmake_minimum_required(VERSION 3.5)
project(lab3)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY config images launch meshes rviz urdf
  DESTINATION share/${PROJECT_NAME}
)

install(
  DIRECTORY config launch rviz urdf
  DESTINATION share/${PROJECT_NAME}
)

install(
  PROGRAMS scripts/ForwardKin.py
  DESTINATION lib/${PROJECT_NAME}
)

install(
  PROGRAMS scripts/DobotKin.py
  DESTINATION lib/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()