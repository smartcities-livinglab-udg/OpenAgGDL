#!/usr/bin/env python
import rospy
# mensajes tipo Int
#from openaggdl.msg import IntR
from std_msgs.msg import Float64
# ------- Sensores
"""[requiered]sudo pip install tsl2561"""
"""[requiered]sudo pip install adafruit_gpio"""  
from tsl2561 import TSL2561
    
if __name__ == '__main__':
    rospy.init_node("sensor_tsl2561")
    rate = rospy.get_param("~rate_hz", 1)
    base_parms = "/var_types/environment_variables/{}"
    r = rospy.Rate(rate)

    sensor = TSL2561()

    tsl2561_pub = rospy.Publisher("light_intensity/raw", Float64, queue_size=10)
    
    while not rospy.is_shutdown():

        data = sensor.lux()
        rospy.loginfo("light_intensity/raw : [{}]".format(data))
        
        if data is not None:
            tsl2561_pub.publish(data)
            rospy.set_param(base_parms.format("light_intensity/last_value"), data)
        
        r.sleep()