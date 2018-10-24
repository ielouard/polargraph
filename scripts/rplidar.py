#!/usr/bin/env python
# coding=utf-8

'''
    File name: limit_service_node.py
    Author: Ibrahim elouard
    Date created: 16/10/2018
    Date last modified: 16/10/2018
    Python Version: 2.7
'''

import rospy, time
import math
from sensor_msgs.msg import LaserScan
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean
from geometry_msgs.msg import Pose2D

class coord():
    def __init__(self,x,y):
        self.x=x
        self.y=y

class Command():
    '''
        TODO
    '''
    bord_min=0.6
    bord_max=10.2
    pos_pub=rospy.Publisher("/pose",Pose2D, queue_size=1)
    pos_msg=Pose2D()
    def __init__(self):
        '''
            Fonction d'initialisation du noeud
        '''
        rospy.init_node('command_node')
        rospy.Subscriber("/scan", LaserScan, self.command_callback)
        rospy.spin()


    def command_callback(self,scan):
        '''
            Fonction de callback du subscriber au topic /range_data
        '''
        posX=[]
        posY=[]
        angles=[]
        for idx,val in enumerate(scan.ranges):
            angle= scan.angle_min+(scan.angle_increment*idx)
            if not math.isinf(val) and val < 1 and angle>(-3.14/4) and angle<(3.14/4):
                #rospy.loginfo("Range:%s , theta: %s", val,angle)
                #rospy.loginfo("X: %s   | Y: %s", math.cos(angle)*val, math.sin(angle)*val)
                posX.append(math.cos(angle)*val)
                posY.append(math.sin(angle)*val)
                angles.append(angle)
                # time.sleep(0.01)
                # print("\033c")
        if posX and posY:
            self.pos_msg.x=mean(posX)
            self.pos_msg.y=mean(posY)
            self.pos_msg.theta=mean(angles)
            self.pos_pub.publish(self.pos_msg)
            rospy.loginfo("X: %.2f   | Y: %.2f", mean(posX),mean(posY))





if __name__ == "__main__":
    tr=Command()
