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
from sensor_msgs.msg import Range

class Command():
    '''
        TODO
    '''
    collision=False
    bord_min=0.6
    bord_max=10.2
    def __init__(self):
        '''
            Fonction d'initialisation du noeud
        '''
        rospy.init_node('command_node')
        rospy.Subscriber("/range_data", Range, self.command_callback)
        rospy.spin()


    def command_callback(self,pose):
        '''
            Fonction de callback du subscriber au topic /range_data
        '''
        rospy.loginfo("Sensor: %s, Range:%s mm",pose.header.frame_id, pose.range)


if __name__ == "__main__":
    tr=Command()
