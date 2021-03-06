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
from std_msgs.msg import Float64MultiArray

class Command():
    '''
        TODO
    '''
    collision=False
    bord_min=0.6
    bord_max=10.2
    previous_X=0
    previous_Y=0
    motor_pub=None
    cmd_msg= Float64MultiArray()
    def __init__(self):
        '''
            Fonction d'initialisation du noeud
        '''
        rospy.init_node('command_node')
        rospy.Subscriber("/range_data", Range, self.command_callback)
        self.motor_pub=rospy.Publisher("/motor_cmd", Float64MultiArray)
        rospy.spin()


    def command_callback(self,pose):
        '''
            Fonction de callback du subscriber au topic /range_data
        '''
        if pose.range < 300 and pose.range>70:
            if pose.header.frame_id=="Sensor1":
                if pose.range > 150:
                    rospy.loginfo("up")
                    self.cmd_msg.data=[-1.0,1.0]
                    self.motor_pub.publish(self.cmd_msg)
                elif pose.range < 150:
                    self.cmd_msg.data=[1.0,-1.0]
                    self.motor_pub.publish(self.cmd_msg)

                    rospy.loginfo("Down")
                self.previous_Y=pose.range
            else:
                if pose.range > 150 :
                    self.cmd_msg.data=[1.0,1.0]
                    self.motor_pub.publish(self.cmd_msg)
                    rospy.loginfo("Left")
                elif pose.range < 150:
                    self.cmd_msg.data=[-1.0,-1.0]
                    self.motor_pub.publish(self.cmd_msg)
                    rospy.loginfo("Right")
                self.previous_X=pose.range

            rospy.loginfo("Sensor: %s, Range:%s mm",pose.header.frame_id, pose.range)


if __name__ == "__main__":
    tr=Command()
