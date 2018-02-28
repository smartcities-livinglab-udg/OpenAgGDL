#!/usr/bin/env python
"""
el sensor HTU2DF obtiene la temperatura del ambiente
asi como la humedad del aire
"""
import rospy, time
from std_msgs.msg import Float64
from libs.HTU21DF import HTU21D

#TODO: validar sensor conectado, elegir que topico publicar
def set_param(param_name, value):
	rospy.set_param(param_name, value)

if __name__ == '__main__':
	rospy.init_node("sensor_htu21d")
	rate = rospy.get_param("~rate_hz", 1)
	r = rospy.Rate(rate)
	base_parms = "/var_types/environment_variables/{}"

	sensor = HTU21D()

	htu21d_temp_pub = rospy.Publisher("air_temperature/raw", Float64, queue_size=10)
	htu21d_hum_pub = rospy.Publisher("air_humidity/raw", Float64, queue_size=10)

	while not rospy.is_shutdown():

		data_temp = sensor.read_temperature()
		rospy.loginfo("air_temperature/raw : [{}]".format(data_temp))
		data_hum = sensor.read_humidity()
		rospy.loginfo("air_humidity/raw : [{}]".format(data_hum))
		
		if data_temp is not None:
			htu21d_temp_pub.publish(data_temp)
			set_param(base_parms.format("air_temperature/last_value"), data_temp)
		
		if data_hum is not None:
			htu21d_hum_pub.publish(data_hum)
			set_param(base_parms.format("air_humidity/last_value"), data_hum)
			
		r.sleep()