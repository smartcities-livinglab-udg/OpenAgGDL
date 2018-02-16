#!/usr/bin/env python
"""[requiered]sudo pip install tsl2561"""
"""[requiered]sudo pip install adafruit_gpio"""        
import rospy
# mensajes tipo Int
from openaggdl.msg import IntR
# ------- Sensores
from tsl2561 import TSL2561

class TSL2561_Tlkr:
    """LIGHT TO DIGITAL CONVERTER Talker"""
    """"""
    def __init__(self):        
        # Instancia de configuracion
        self.tsl = TSL2561()

    # metodo para leer el registro del sensor
    def read_tsl2561(self):
        response = int(self.tsl.lux())
                
        return response


    def run(self):
        #Topico para comunicar mensajes
        pub = rospy.Publisher("light_sensor", IntR, queue_size=10)
        # nombre del nodo
        rospy.init_node("TSL2561_Tlkr", anonymous=True)
        
        rate = rospy.Rate(10) # 10hz

        while not rospy.is_shutdown():
            response = self.read_tsl2561()
            print response
            rospy.loginfo(response)

            msg = IntR()
            msg.header.stamp = rospy.Time.now()
            msg.data = response

            pub.publish(msg)

            rate.sleep()

    
if __name__ == '__main__':
    try:
        init = TSL2561_Tlkr()
        init.run()
    except rospy.ROSInterruptException as e:
        print ("Error al correr TSL2561_Tlkr.py " )
        print e
