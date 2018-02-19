#!/usr/bin/env python
"""
el sensor HTU2DF obtiene la temperatura del ambiente
asi como la humedad del aire
"""

import rospy, time
from libs.HTU21DF import HTU21D

while True:
    print HTU21D(1).read_temperature()

#TODO: validar sensor conectado

if __name__ == '__main__':
	rospy.init_node("sensor_htu21d")
	sense_temp = rospy.get_param("~temp", True)
	rate = rospy.get_param("~rate_hz", 1)
	r = rospy.Rate(rate)
	
	if sense_temp:
		htu21d_pub = rospy.Publisher("air_temperature/raw", Float64, queue_size=10)
	else:
		htu21d_pub = rospy.Publisher("air_humidity/raw", Float64, queue_size=10)

	#@param : i2c y
	with HTU21D(1) as sensor:
		while not rospy.is_shutdown():
			data = sensor.read_temperature()
			if data in not None:
				htu21d_pub.publish(data)

			r.sleep()