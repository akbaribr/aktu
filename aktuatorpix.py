#!/usr/bin/python3

import rospy
import time
from std_msgs.msg import Float64, Float32, Int32, Bool
from geometry_msgs.msg import TwistStamped
from mavros_msgs.msg import VFR_HUD, OverrideRCIn
from mavros_msgs.srv import SetMode

LOOP_RATE = 1
TARGET_RADIUS = 1.2
DROP_MECHANISM_CHANNEL = 3
DROP_MECHANISM_PWMS = [1500, 1250, 1750]
if __name__ == '__main__':
  # initialize ros node
  rospy.loginfo('Initializing dropping_mechanism_test.py...')
  rospy.loginfo('Initializing dropping_mechanism_test node...')
  rospy.init_node('dropping_mechanism_test', anonymous=True)

  # initialize target loop rate
  rate = rospy.Rate(LOOP_RATE)
  
  # initializing publishers
  rospy.loginfo('Initializing publishers...')

  override_rc_in_pub = rospy.Publisher('/mavros/rc/override', OverrideRCIn, queue_size=10)
  # center the servo
  override_rc_in_msg = OverrideRCIn()
  override_rc_in_msg.channels[DROP_MECHANISM_CHANNEL] = DROP_MECHANISM_PWMS[0]
  override_rc_in_pub.publish(override_rc_in_msg)

  # main loop
  rospy.loginfo('dropping_mechanism_test.py initialization complete')
  cur_state_index = 0
  while not rospy.is_shutdown():
    if cur_state_index == 0:
      rospy.loginfo('SERVO MID')
    elif cur_state_index == 1:
      rospy.loginfo('LEFT')
    else:
      rospy.loginfo('RIGHT')
    override_rc_in_msg = OverrideRCIn()
    override_rc_in_msg.channels[DROP_MECHANISM_CHANNEL] = DROP_MECHANISM_PWMS[cur_state_index]
    override_rc_in_pub.publish(override_rc_in_msg)
    cur_state_index = (cur_state_index + 1) % len(DROP_MECHANISM_PWMS)

    time.sleep(1)


  rospy.loginfo('Shutting down dropping_mechanism_test.py...')
  rospy.loginfo('dropping_mechanism_test.py is shut down')
