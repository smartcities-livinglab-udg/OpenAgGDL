#!/usr/bin/env python
"""
el sensor HTU2DF obtiene la temperatura del ambiente
asi como la humedad del aire
"""
import rospy, time
from std_msgs.msg import Float64
from libs.HTU21DF import HTU21D

#TODO: validar sensor conectado, elegir que topico publicar

if __name__ == '__main__':
	rospy.init_node("sensor_htu21d")
	rate = rospy.get_param("~rate_hz", 1)
	r = rospy.Rate(rate)

	sensor = HTU21D()

	htu21d_temp_pub = rospy.Publisher("air_temperature/raw", Float64, queue_size=10)
	htu21d_hum_pub = rospy.Publisher("air_humidity/raw", Float64, queue_size=10)

	while not rospy.is_shutdown():

		data_temp = sensor.read_temperature()
		data_hum = sensor.read_humidity()
		
		if data_temp is not None:
			htu21d_temp_pub.publish(data_temp)
		
		if data_hum in not None:
			htu21d_hum_pub.publish(data_hum)
			
		r.sleep()