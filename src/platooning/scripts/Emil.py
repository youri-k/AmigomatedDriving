#!/usr/bin/python

import rospy
from aruco_msgs.msg import MarkerArray
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
import math



command_velocity_publisher = None

in_range = False
cmd_vel = Twist()
lastMarkerSignal = 0
slave_last_seconds = []


def callback_marker(data):
    #command_velocity_publisher.publish(data.twist.twist)
    global in_range
    global lastMarkerSignal
    global slave_last_seconds
    for marker in data.markers:
        if marker.id == 101 or marker.id == 102:
            lastMarkerSignal = marker.header.stamp
            slave_last_seconds = []
            distance_front = marker.pose.pose.position.z
            rospy.loginfo(distance_front)
            if distance_front < 0.6:
                in_range = True
                rospy.loginfo("in_range = true")
                # cmd_vel.linear.x = pow((distance_front - 0.4) / 2,3) * 20
            else:
                rospy.loginfo("Out of range")
                rospy.loginfo("Bild basiert")
                cmd_vel.linear.x = distance_front - 0.4
                in_range = False
                rospy.loginfo("in_range = false")
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
    global slave_last_seconds
    if rospy.get_rostime()-lastMarkerSignal > 4:
        sendForHelpPlease()
    else:
        slave_last_seconds.append([rospy.get_rostime(), cmd_vel])
        command_velocity_publisher.publish(cmd_vel)

def sendForHelpPlease():
    global slave_last_seconds
    rospy.loginfo("Mayday Mayday!")
    rospy.loginfo(slave_last_seconds)

if __name__ == '__main__':

    rospy.init_node('platooning_follow_planner', anonymous=True)
    rospy.Subscriber("web_cam/aruco_marker_publisher/markers", MarkerArray, callback_marker)
    rospy.Subscriber("/Achim/RosAria/pose", Odometry, callback_master)
    command_velocity_publisher = rospy.Publisher('RosAria/cmd_vel', Twist, queue_size=10)

    rospy.spin()
