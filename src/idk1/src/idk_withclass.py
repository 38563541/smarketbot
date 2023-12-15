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

class Commander:
    def __init__(self):
        rospy.init_node('commander', anonymous=True)
        self.rate = rospy.Rate(0.0636) # 0.1hz
        self.velocity_publisher = rospy.Publisher('/move_base/goal', MoveBaseActionGoal, queue_size=10)
        self.rbt_status = ""

    def move(self):
        #Receiveing the user's input
        print("Let's move your marslite.")
        x = int(input("input x: "))
        y = int(input("input y: "))
        z = int(input("input z: "))
        w = int(input("input w: "))
        print(x,y,z,w)
        print("start sending")
        rospy.loginfo('start sending msg...')
        self.publisher_node(x, y, z, w)
        print("end sending")
        rospy.loginfo('end sending msg...')

    def subscriber_node(self):
        print('start subscribing')
        rospy.Subscriber("/move_base/result", MoveBaseActionResult, self.callback)
        print('end subscribing')

    def callback(self, data):
        self.rbt_status = data.status.text
        print(self.rbt_status)

    def publisher_node(self, x, y, z, w):
        cmd = MoveBaseActionGoal()
        cmd.goal.target_pose.header.frame_id = 'map'
        cmd.goal.target_pose.pose.position.x = x
        cmd.goal.target_pose.pose.position.y = y
        cmd.goal.target_pose.pose.orientation.z = z
        cmd.goal.target_pose.pose.orientation.w = w
        self.velocity_publisher.publish(cmd)
    
    def run(self):
        while not rospy.is_shutdown():
            print('start running')
            rospy.sleep(2.)
            self.move()            
            self.rate.sleep()
            self.subscriber_node()
            while(self.rbt_status == ""):
                self.subscriber_node()
            
            self.rbt_status = ""

            #input("Press Enter to continue...")
        
        rospy.spin()
        print('end running')


#################################################################

if __name__ == '__main__':
    commander = Commander()
    try:
        commander.run()
    except rospy.ROSInterruptException: 
        pass
