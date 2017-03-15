#!/usr/bin/python

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry



command_velocity_publisher = None #Publisher
velocity = None #Twist


def callback(data):
    velocity = data.twist.twist
    setMovement(velocity)    

def abstandsKontrolle(abstand):
    soll_Abstand = 0.1
    if abstand > soll_Abstand:
        velocity.linear.x *= 1.1
    if abstand < soll_Abstand:
        velocity.linear.x *= 0.9
    
    setMovement(velocity)

def setMovement(velocity):
    command_velocity_publisher.publish(velocity)

if __name__ == '__main__':

    rospy.init_node('platooning_follow_planner', anonymous=True)
    rospy.Subscriber("/Achim/RosAria/pose", Odometry, callback)
    command_velocity_publisher = rospy.Publisher('RosAria/cmd_vel', Twist, queue_size=10)

    x = 2
    while x > -2:
        abstandsKontrolle(x)
        x -= 0.3
        sleep(400)

    rospy.spin()



