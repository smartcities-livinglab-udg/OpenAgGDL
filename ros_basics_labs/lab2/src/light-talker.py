#!/usr/bin/env python
import rospy
from std_msgs.msg import String
#"""The smbus package contains the classes used for I2C 
#communication. At the top of the Python script add the line"""
import smbus

#"""Variables de configuracion"""
LIN_LUM_ADDR = 0x39 # Direccion para leer sensor de iluminacion 0
LIN_LUM_REG_CTRL_VALUE_L = 0x0C
LIN_LUM_REG_CTRL_VALUE_H = 0x0D
bus = smbus.SMBus(1)


#"""metodo para leer el registro del sensor"""
def read_lum_reg(register):
    H = bus.read_byte_data(LIN_LUM_REG_CTRL_VALUE_H, register) << 8
    L = bus.read_byte_data(LIN_LUM_REG_CTRL_VALUE_L, register)
    MASK_REG = L | H
    return  MASK_REG

def run():
    #Topico para comunicar mensajes
    pub = rospy.Publisher("light_sensor", String, queue_size=10)
    # nombre del nodo
    rospy.init_node("light-talker", anonymous=True)
    
    rate = rospy.Rate(10) # 10hz

    while not rospy.is_shutdown():
        response = read_lum_reg(LIN_LUM_REG_CTRL_VALUE_L)
        rospy.loginfo(response)
        pub.publish(response)
        rate.sleep()

    
if __name__ == '__main__':
    try:
        run()
    except rospy.ROSInterruptException:
        pass