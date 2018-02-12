#!/usr/bin/python
"""
control Pumps [relays]
Algorithms across I2C

Requirements:

* 670 activaciones durante el dia, 
* periodos activos de 20 a 60 segundos, 
* alternar entre dos depositos de sustancia distintos

by rasztul 2017

"""
import rospy
from std_msgs.msg import String
from gpiozero import LED
import sys, argparse
import time 

SECONDS_IN_A_DAY = 60 * 60 * 24
OUTPUT1 = LED(17)
OUTPUT2 = LED(18)

def setOutput(out, pub):
	if out == True:
		OUTPUT1.on()
		hello_str = "GPIO ON %s" % rospy.get_time()
		rospy.loginfo(hello_str)
		pub.publish(hello_str)
		#OUTPUT2.on()
	else:
		OUTPUT1.off()
		hello_str = "GPIO Off %s" % rospy.get_time()
		rospy.loginfo(hello_str)
		pub.publish(hello_str)
		#OUTPUT2.off()
		
def sleep(seconds):
	#Tiempo de inactividad
	time.sleep(seconds)

# def validate(cycles, timeOn):
# 	okGo = True if ((cycles * timeOn) <= SECONDS_IN_A_DAY) else False
	
# 	if okGo:
# 		run(cycles, timeOn)
# 	else:
# 		msg = "\n--- CUIDADO ---"
# 		msg = msg + "\nPara " + str(cycles) + " ciclos en " + str(timeOn) + " s Todo el dia seria un ciclo"
# 		init(msg)

def calculateTimeOff(cycles, timeOn):
	timeOff = SECONDS_IN_A_DAY / cycles
	return timeOff - timeOn

def run(cycles, timeOn, pub):
	while True:
		setOutput(True, pub)
		sleep(calculateTimeOff(cycles, timeOn))
		setOutput(False, pub)
		sleep(calculateTimeOff(cycles, timeOn))

# def init(msg):
# 	print msg, "\n"
# 	cycles = input("Indica los ciclos por dia : ") 
# 	timeOn = input("Indica la duracion de actividad para cada ciclo [en segundos] : ")

# 	validate(cycles, timeOn)

def talker():
    pub = rospy.Publisher('gpio_chatter', String, queue_size=10)
    rospy.init_node('talkerGPIO', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
    	run(20, 60, pub)
        rate.sleep()
	
if __name__ == '__main__':
	print "Bienvenido [ Control de ciclos y tiempos ]"
	try:
		talker()
	except rospy.ROSInterruptException:
		pass