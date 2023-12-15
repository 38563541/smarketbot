#!/usr/bin/env python3

'''
REMIND: you should roslaunch some of the files before using this code.
This code can control MARS to go to a desired position.
First, you have to set rviz to make MARS realize its position in the room.
By moving MARS to the position and getting its coordinate from "rostopic echo /amcl_pose", then, setting the x, y, z, w to move to the place.  
'''

import rospy
from move_base_msgs.msg import MoveBaseActionResult
from move_base_msgs.msg import MoveBaseActionGoal

def move():

    # Starts a new node
    rospy.init_node('plat_move', anonymous=True)
    velocity_publisher = rospy.Publisher('/move_base/goal', MoveBaseActionGoal, queue_size=10)

    cmd = MoveBaseActionGoal()
    rate = rospy.Rate(0.0636) # 0.1hz

    #Receiveing the user's input
    print("Let's move your marslite.")
    x = int(input("input x"))
    y = int(input("input y"))
    z = int(input("input z"))
    w = int(input("input w"))
    print(x,y,z,w)

    while not rospy.is_shutdown():

        rospy.sleep(2.)
        # raw_input("Press Enter to continue...")
        print("sending")
        cmd.goal.target_pose.header.frame_id = 'map'
        cmd.goal.target_pose.pose.position.x = x
        cmd.goal.target_pose.pose.position.y = y
        cmd.goal.target_pose.pose.orientation.z = z
        cmd.goal.target_pose.pose.orientation.w = w
        velocity_publisher.publish(cmd)
        print(type(cmd.goal.target_pose.pose.position.x))
        rospy.loginfo('is sending msg...')
        rate.sleep()
        input("Press Enter to continue...")

def callback(data):
    text = data.status.text
    rospy.loginfo(f"Text: {text}")
    print(text)

def subscriber_node():
    print("read gogo")
    rospy.init_node('result_read', anonymous=True)
    rospy.Subscriber("/move_base/result", MoveBaseActionResult, callback)
    rospy.spin()       
#################################################################

if __name__ == '__main__':
    try:
        #Testing our function
        move()
        subscriber_node()

    except rospy.ROSInterruptException: pass
