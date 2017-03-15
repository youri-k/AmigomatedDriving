#!/usr/bin/python

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry



command_velocity_publisher = None


def callback(data):
    command_velocity_publisher.publish(data.twist.twist)
    

if __name__ == '__main__':

    rospy.init_node('platooning_follow_planner', anonymous=True)
    rospy.Subscriber("/Achim/RosAria/pose", Odometry, callback)
    command_velocity_publisher = rospy.Publisher('RosAria/cmd_vel', Twist, queue_size=10)

    rospy.spin()
