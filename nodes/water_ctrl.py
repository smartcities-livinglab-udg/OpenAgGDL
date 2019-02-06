#!/usr/bin/python
"""
	En este script se controla la bomba de 5v,
	y las valvulas conectadas a relevadores
"""
import rospy
import time
from std_msgs.msg import Float64
import RPi.GPIO as GPIO#Importa la libreria GPIO / Permite usar interfaces

VALVE_1 = 36
VALVE_2 = 38
VALVE_3 = 35
PUMP = 37
POWER_OFF = True

def cicle():
	#sin encender la bomba se abre la V3
	GPIO.output(VALVE_3, not POWER_OFF)
	time.sleep(4)
	#Se cierra V3
	GPIO.output(VALVE_3, POWER_OFF)
	#Se enciende Bomba
	GPIO.output(PUMP, not POWER_OFF)
	#Se abre V2
	GPIO.output(VALVE_2, not POWER_OFF)
	time.sleep(5)
	#Se cierra V2
	GPIO.output(VALVE_2, POWER_OFF)
	#Se abre V1
	GPIO.output(VALVE_1, not POWER_OFF)
	time.sleep(5)
	#Se cierra V1 
	GPIO.output(VALVE_1, POWER_OFF)
	#Se apaga Bomba
	GPIO.output(PUMP, POWER_OFF)
	
	return False

def setup(PINES):
	#OUTPUTS = PINES
	GPIO.setmode(GPIO.BOARD) #Inicializamos la tarjeta con la numeracion fisica/eleccion de los pines modo board
	GPIO.setwarnings(False)
	for _pin in PINES:
		GPIO.setup(_pin, GPIO.OUT)
	allOff(PINES)

def allOff(PINES):
	for _pin in PINES:
		GPIO.output(_pin, POWER_OFF)

def hardOff(outs):
	#rospy.logwarn("hardOff")
	allOff(outs)

#startAutoIrrigation(Boolean, seconds, array):
def startAutoIrrigation(Irrigation, Periodicity, outs):
	setup(outs)
	while True:
		while (Irrigation):
			Irrigation = cicle()
		time.sleep(Periodicity)
		Irrigation = True
	allOff(outs)

if __name__ == '__main__':
	
	try:
		rospy.init_node("control", disable_signals=True) #disable_signals=True) permite capturar la excepcion KeyboardInterrupt
		outs = [VALVE_1, VALVE_2, VALVE_3, PUMP]
		startAutoIrrigation(True, 86400, outs)
		#rospy.on_shutdown(hardOff)
		rospy.spin()
	except KeyboardInterrupt:
		hardOff(outs)
	
