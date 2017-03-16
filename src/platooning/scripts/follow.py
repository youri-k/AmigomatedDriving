#!/usr/bin/python


import argparse

parser = argparse.ArgumentParser(description='Follow other AmigoBot')
parser.add_argument('this_name',  type=str, 
                    help='Name of this robot')
parser.add_argument('leading_name',  type=str, 
                    help='Name of the robot directly in front of us')
parser.add_argument('leading_name',  type=str, 
                    help='Name of the master robot')

args = parser.parse_args()


class RobotInfo:
    def __init__(self, namespace, id_marker_left, id_marker_back, id_marker_right):
        self.namespace =         namespace
        self.id_marker_left =    id_marker_left
        self.id_marker_back =    id_marker_back
        self.id_marker_right =   id_marker_right


robot_info = {
    "Achim" : RobotInfo("Achim", 0, 102, 0),
}

print("sending output to " + robot_info[args.this_name].namespace)
