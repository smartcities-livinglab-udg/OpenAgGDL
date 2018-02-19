#!/usr/bin/env python
import rospy
# mensages tipo float[]
from openaggdl.msg import Floats
# ------- Sensores
from libs.MPL115 import MPL115 

class MPL115_Tlkr:
    """Barometer Talker"""
    """"""
    def __init__(self):
        # Instancia de configuracion
        self.barometer = MPL115()

    # metodo para leer el registro del sensor
    def read_barometer(self):
        data = self.barometer.readData()
        a_hpa = self.barometer.readHpa(212.0)

        response = [float(data['temp']), float(data['hpa']), float(a_hpa)]
        
        return response


    def run(self):
        #Topico para comunicar mensajes
        pub = rospy.Publisher("temp_sensor", Floats, queue_size=10)
        # nombre del nodo
        rospy.init_node("MPL115_Tlkr", anonymous=True)
        
        rate = rospy.Rate(10) # 10hz
        #layout = self.layout()

        while not rospy.is_shutdown():
            response = self.read_barometer()
            print response
            rospy.loginfo(response)
            pub.publish(response)
            rate.sleep()

    
if __name__ == '__main__':
    try:
        init = MPL115_Tlkr()
        init.run()
    except rospy.ROSInterruptException as e:
        print ("Error al correr MPL115_Tlkr.py " )
        print e
