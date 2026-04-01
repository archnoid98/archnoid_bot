cmake_minimum_required(VERSION 3.5)
project(archnoid_bot)

# Default to C99
if(NOT CMAKE_C_STANDARD)
  set(CMAKE_C_STANDARD 99)
endif()

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

# --- NEW: Install Python Scripts ---
# This makes 'ros2 run archnoid_bot <script_name>' work
install(PROGRAMS
  scripts/object_detector.py
  scripts/object_follower.py
  DESTINATION lib/${PROJECT_NAME}
)

# Install resource directories
# Note: Adding 'launch' here ensures tracker.launch.py is included
install(
  DIRECTORY config description launch worlds maps
  DESTINATION share/${PROJECT_NAME}
)

# --- IMPORTANT ---
# This must be the last line
ament_package()