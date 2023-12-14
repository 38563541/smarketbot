#!/usr/bin/env python3

import rospy
from move_base_msgs.msg import MoveBaseActionResult

def callback(data):
    text = data.status.text
    rospy.loginfo(f"Text: {text}")

def subscriber_node():
    rospy.init_node('result_read', anonymous=True)
    rospy.Subscriber("/move_base/result", MoveBaseActionResult, callback)
    rospy.spin()

if __name__ == '__main__':
    subscriber_node()
