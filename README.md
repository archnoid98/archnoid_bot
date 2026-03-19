ssh archnoid@192.168.68.137

cd ~/robot_ws
source install/setup.bash

######### KEYBOARD #############
=>Jetson Orin:

ros2 launch archnoid_bot teleop.launch.py

ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r /cmd_vel:=/cmd_vel_key




ros2 run teleop_twist_keyboard  teleop_twist_keyboard  --ros-args -r /cmd_vel:=/diff_cont/cmd_vel_unstamped

     I
  J  K  L
     ,


#########Simulation#############

colcon build --symlink-install
source install/setup.bash

=>Gazebo + ALL:
ros2 launch archnoid_bot launch_sim.launch.py

ros2 launch archnoid_bot launch_sim.launch.py world:=./src/archnoid_bot/worlds/obstacles.world 



ros2 run joint_state_publisher_gui joint_state_publisher_gui 


=> rviz2  urdf publisher:
ros2 launch archnoid_bot rsp.launch.py <- Robot URDF Publisher ->
ros2 launch archnoid_bot rsp.launch.py use_sim_time:=true


rviz2 -d dev_ws/src/archnoid_bot/config/view_bot.rviz 


ros2 launch gazebo_ros gazebo.launch.py <- Empty Gazebo
ros2 run gazebo_ros spawn_entity.py -topic robot_description -entity bot_name <- spawn bot


########github#########
--> go to dev_ws/src/archnoid_bot
git statuts
git add .
git commit -m ""
git push


git pull origin main






############ MOTOR SETUP ################

=> JETSON ORIN:

ros2 run serial_motor_demo driver --ros-args -p serial_port:=/dev/ttyACM0 -p baud_rate:=57600 -p loop_rate:=30 -p encoder_cpr:=362

=> Dev Machine:

ros2 run serial_motor_demo gui



############ LIDAR SETUP ################

=> JETSON ORIN:

ros2 launch archnoid_bot rplidar.launch.py
  
killall rplidar_composition <- kill the lidar

=> Dev Machine:

ros2 service call /stop_motor std_srvs/srv/Empty {} <- Lidar motor stop
ros2 service call /start_motor std_srvs/srv/Empty {} <- Lidar motor start

##################### CAMERA [Must change the IP {camera.launch.py & esp32_cam_bridge->came_node.py} -via arduinoIDE SerialPrint] ###########################

=> JETSON ORIN:

ros2 launch archnoid_bot camera.launch.py

=> Dev Machine:

ros2 run rqt_image_view rqt_image_view <- Camera Feed View
  
  
  
  
#############  ROS2 CONTROL  ####################

ros2 control list_hardware_interfaces <- will show the available command_interface & 													 	 
								 state_interface

ros2 control list_controllers 




#############  ROBOT CONTROL  ####################

=> Jetson Orin:

ros2 launch archnoid_bot launch_robot.launch.py



#############  SLAM  ####################

=> Jetson Orin:

ros2 launch slam_toolbox online_async_launch.py params_file:=./src/archnoid_bot/config/mapper_params_online_async.yaml use_sim_time:=false



  
####info#####

BAUDRATE     57600
encoder_cpr:        362
motor_max_rpm:      315
wheel_diameter:     0.12 m   (wheel is 0.06m radius)

==>Camera:
Connected! IP: 192.168.68.126
WebSocket server started on port 81


===> Stop All ROS Nodes : sudo pkill -9 -f ros2

###########################################################################

ros2 launch archnoid_bot localization_launch.py
ros2 launch archnoid_bot navigation_launch.py


################################ MAP  #################################

ros2 run nav2_map_server map_saver_cli -f ~/robot_ws/src/archnoid_bot/maps/my_room -> .pgm & .yaml

ros2 service call /slam_toolbox/serialize_map slam_toolbox/srv/SerializePoseGraph "filename: '/home/archnoid/robot_ws/src/archnoid_bot/maps/my_room_serial'" -> Serialize MAP
	


