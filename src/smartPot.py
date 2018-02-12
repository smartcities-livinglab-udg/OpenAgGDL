#!/usr/bin/env python
import rospy
import message_filters
from openaggdl.msg import Floats, FloatsR, IntR
from std_msgs.msg import Int64

#-------- LISTENERS ---------
from LightLstnr_SmartPot import LightLstnr_SmartPot
from TempLstnr_SmartPot import TempLstnr_SmartPot

LIGHT_CHANNEL = "light_sensor"
TEMP_CHANNEL = "temp_sensor"

class SmartPot:

    def __init__(self):
        self.LIGHT_CHANNEL = LIGHT_CHANNEL
        self.TEMP_CHANNEL = TEMP_CHANNEL

    def filterLux(self, lux):

        response = ""

        if(lux > 20):
            response = ('Ahhhh its too much light >w< [ %s ]', lux)
        elif(lux > 16 and lux < 20):
            response = ('Nice =D [ %s ]', lux)
        else:
            response = ('Well ok n.n [ %s ]', lux)

        return response


    def filterTemp(self, temp):

        response = ""
        
        if(temp > 20):
            response = ('Ahhhh its hot >w< [ %s C]', temp)
        elif(temp > 16 and temp < 20):
            response = ('Nice =D [ %s C]', temp)
        else:
            response = ('Well ok n.n [ %s C]', temp)

        return response

    def callback(self, dataTemp, dataLight):
        resLux = self.filterLux(dataLight.data)
        resTemp = self.filterTemp(dataTemp.data[0])
        rospy.loginfo(rospy.get_caller_id() + ' Smart Pot says \r\n [ABOUT_LIGHT] %s \r\n [ABOUT_TEMP] %s ', resLux, resTemp)

    def listener(self):
        rospy.init_node('SmartPot', anonymous=True)

        dataTemp = message_filters.Subscriber(self.TEMP_CHANNEL, FloatsR)
        dataLight = message_filters.Subscriber(self.LIGHT_CHANNEL, IntR)

        ts = message_filters.TimeSynchronizer([dataTemp, dataLight], 10)
        ts.registerCallback(self.callback)

        rospy.spin()
        
        

if __name__ == '__main__':
    try:
        init = SmartPot()
        init.listener()
        
        
    except rospy.ROSInterruptException as e:
        print ("Error al correr SmartPot.py " )
        print e

