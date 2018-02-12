#!/usr/bin/env python
import rospy
from std_msgs.msg import String
# ------- Sensores
from libs.MPL115 import MPL115 
#"""The smbus package contains the classes used for I2C 
#communication. At the top of the Python script add the line"""
import smbus

class MPL115_Tlkr:
    """Barometer Talker"""
    """"""
    def __init__(self):
        # Instancia de configuración
        self.barometer = MPL115()

    # metodo para leer el registro del sensor
    def read_barometer(self):
        data  = self.barometer.readData()
        a_hpa = self.barometer.readHpa(212.0)

        response = {"data":data, "a_hpa":a_hpa}

        return response


    def run(self):
        #Topico para comunicar mensajes
        pub = rospy.Publisher("temp_sensor", String, queue_size=10)
        # nombre del nodo
        rospy.init_node("light_talker", anonymous=True)
        
        rate = rospy.Rate(10) # 10hz

        while not rospy.is_shutdown():
            #response = self.hexToBin(self.read_lum_reg())
            response = self.read_lum_reg()
            rospy.loginfo(response)
            pub.publish(response)
            rate.sleep()

    
if __name__ == '__main__':
    try:
        init = MPL115_Tlkr()
        init.run()
    except rospy.ROSInterruptException as e:
        print ("Error la correr MPL115_Tlkr.py " )
        print e
