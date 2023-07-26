# CMake generated Testfile for 
# Source directory: /home/icetea0113/ros2_ws/src/YDLidar-SDK/python
# Build directory: /home/icetea0113/ros2_ws/src/YDLidar-SDK/build/python
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(ydlidar_py_test "/usr/bin/python" "/home/icetea0113/ros2_ws/src/YDLidar-SDK/python/test/pytest.py")
set_tests_properties(ydlidar_py_test PROPERTIES  ENVIRONMENT "PYTHONPATH=/opt/ros/foxy/lib/python3.8/site-packages:/home/icetea0113/ros2_ws/src/YDLidar-SDK/build/python" _BACKTRACE_TRIPLES "/home/icetea0113/ros2_ws/src/YDLidar-SDK/python/CMakeLists.txt;42;add_test;/home/icetea0113/ros2_ws/src/YDLidar-SDK/python/CMakeLists.txt;0;")
subdirs("examples")
