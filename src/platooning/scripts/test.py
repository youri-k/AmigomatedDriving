#!/usr/bin/python

import rospy
from aruco_msgs.msg import MarkerArray
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
import math



command_velocity_publisher = None

in_range = False;
cmd_vel = Twist()


def callback_marker(data):
    #command_velocity_publisher.publish(data.twist.twist)
    for marker in data.markers:
        if marker.id == 101 or marker.id == 102:
            distance_front = marker.pose.pose.position.z
            if distance_front < 0.6:
                in_range = True
                cmd_vel.linear.x = distance_front - 0.4
                # cmd_vel.linear.x = pow((distance_front - 0.4) / 2,3) * 20
                rospy.loginfo("Bild basiert")
            else:
                rospy.loginfo("Out of range")
                in_range = False
            distance_side = marker.pose.pose.position.x
            # rospy.loginfo("Vorne: {}".format(distance_front))
            # rospy.loginfo(distance_side)
            cmd_vel.angular.z = -1.5 * distance_side
            if not in_range:
                setVel()
        elif marker.id == 510:
            cmd_vel.linear.x = 0
            cmd_vel.angular.z = 0
            setVel()
        else:
            rospy.loginfo("Ignoring Marker with wrong ID")

def callback_master(data):
    rospy.loginfo("Received velocity from master")
    if in_range:
        cmd_vel.linear.x = data.twist.twist.linear.x
        rospy.loginfo("Master basiert")
        setVel()

def setVel():
    command_velocity_publisher.publish(cmd_vel)

if __name__ == '__main__':

    rospy.init_node('platooning_follow_planner', anonymous=True)
    rospy.Subscriber("web_cam/aruco_marker_publisher/markers", MarkerArray, callback_marker)
    rospy.Subscriber("/Achim/RosAria/pose", Odometry, callback_master)
    command_velocity_publisher = rospy.Publisher('RosAria/cmd_vel', Twist, queue_size=10)

    rospy.spin()
