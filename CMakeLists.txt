cmake_minimum_required(VERSION 3.8)
project(project_a_description)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)

install(DIRECTORY
  models
  urdf
  worlds
  launch
  scripts
  DESTINATION share/${PROJECT_NAME}
)

# Also install meshes at package root for model:// references in world file
install(DIRECTORY meshes/
  DESTINATION share/${PROJECT_NAME}/meshes
)

install(PROGRAMS
  scripts/wait_and_spawn.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()