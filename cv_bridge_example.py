cd ~/catkin_ws/src
catkin_create_pkg cv_bridge std_msgs rospy roscpp
mkdir -p ~/catkin_ws/src/cv_bridge/scripts
gedit ~/catkin_ws/src/cv_bridge/scripts/cv_bridge_example.py

#!/usr/bin/env python3
  
# Import ROS libraries and messages
  import rospy
  from sensor_msgs.msg import Image

  # Import OpenCV libraries and tools
  import cv2
  from cv_bridge import CvBridge, CvBridgeError

  # Initialize the ROS Node named 'cv_bridge_example' and allow multiple nodes to be run with this name
  rospy.init_node('cv_bridge_example', anonymous=True)

  # Print "Hello ROS!" to the Terminal and to a ROS Log file located in ~/.ros/log/loghash/*.log
  rospy.loginfo("Hello ROS!")

  # Initialize the CvBridge class
  bridge = CvBridge()

  # Define a callback for the Image message
  def image_callback(img_msg):
      
      # log some info about the image topic
      rospy.loginfo(img_msg.header)

      # Try to convert the ROS Image message to a CV2 Image
      try:
          cv_image = bridge.imgmsg_to_cv2(img_msg, "passthrough")
      except CvBridgeError, e:
          rospy.logerr("CvBridge Error: {0}".format(e))

      # Convert the image to Grayscale
      	gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

      # Show the converted image
      cv2.imshow("Image Window", gray)
      cv2.waitKey(3)

  # Initalize a subscriber to the "/camera/rgb/image_raw" topic with the function "image_callback" as a callback
  sub_image = rospy.Subscriber("/camera/rgb/image_raw", Image, image_callback)

  # Initialize an OpenCV Window named "Image Window"
  cv2.namedWindow("Image Window", 1)

  # Loop to keep the program from shutting down unless ROS is shut down, or CTRL+C is pressed
  while not rospy.is_shutdown():
      rospy.spin()

catkin_install_python(PROGRAMS scripts/cv_bridge_example.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)	
chmod +x ~/catkin_ws/src/cv_bridge/scripts/cv_bridge_example.py
cd ~/catkin_ws
catkin_make


roscore

cd ~/catkin_ws
source ~/catkin_ws/devel/setup.bash
rosrun cv_bridge cv_bridge_example.py
