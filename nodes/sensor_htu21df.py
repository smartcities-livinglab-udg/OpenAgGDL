#!/usr/bin/env python
"""
el sensor HTU2DF obtiene la temperatura del ambiente
asi como la humedad del aire
"""
import rospy, time
from std_msgs.msg import Float64
from libs.HTU21DF import HTU21D

#TODO: validar sensor conectado

if __name__ == '__main__':
	rospy.init_node("sensor_htu21d")
	sense_temp = rospy.get_param("~temp", True)
	rate = rospy.get_param("~rate_hz", 1)
	r = rospy.Rate(rate)

	sensor = HTU21D()

	if sense_temp:
		htu21d_pub = rospy.Publisher("air_temperature/raw", Float64, queue_size=10)

		while not rospy.is_shutdown():
			data = sensor.read_temperature()
			if data is not None:
				htu21d_pub.publish(data)

			r.sleep()
	else:
		htu21d_pub = rospy.Publisher("air_humidity/raw", Float64, queue_size=10)

		while not rospy.is_shutdown():
			data = sensor.read_humidity()
			if data is not None:
				htu21d_pub.publish(data)

			r.sleep()