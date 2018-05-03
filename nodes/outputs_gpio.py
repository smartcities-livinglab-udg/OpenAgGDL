#!/usr/bin/python
import rospy
import time
from std_msgs.msg import Float64
import RPi.GPIO as GPIO#Importa la libreria GPIO / Permite sar interfaces

PIN_A = 37 # No de pin del GPIO en la RaspberryPi
PIN_B = 36
PIN_C = 38
PIN_D = 40

class Actuator:
	def __init__(self, pin, environment, topic, topic_type):
		self.environment = environment
		self.pin = pin
		self.topic = topic
		self.sub  = rospy.Subscriber(topic, topic_type, self.on_data)
		
	def on_data(self, item):
		value = item.data
		# This is kind of a hack to correctly interpret UInt8MultiArray
		# messages. There should be a better way to do this
		if item._slot_types[item.__slots__.index('data')] == "uint8[]":
			value = [ord(x) for x in value]

		GPIO.output(self.pin, int(value))
		rospy.logdebug("Actuator.on_data : {} PIN:{}".format(value, self.pin))
		

def createSubcribers( pines, environment, topics ):
	i=0

	for topic_name in topics:
		topic_name = str(topic_name)
		topic = "{}/cmd".format(topic_name) # los actuadores se definen en el archivo lion_var_types
		
		Actuator( pin=pines[i], environment=environment, topic=topic, topic_type=Float64 )
		i+=1


def setup(PINES):
	GPIO.setmode(GPIO.BOARD) #Inicializamos la tarjeta con la numeracion fisica/eleccion de los pines modo board
	GPIO.setwarnings(False)
	for _pin in PINES:
		GPIO.setup(_pin, GPIO.OUT)

if __name__ == '__main__':
	
	rospy.init_node("actuators")
	
	PIN_A = rospy.get_param("~act_a", PIN_A)
	PIN_B = rospy.get_param("~act_b", PIN_B)
	PIN_C = rospy.get_param("~act_c", PIN_C)
	PIN_D = rospy.get_param("~act_d", PIN_D)
	pines = [PIN_A, PIN_B, PIN_C, PIN_D]

	TOPIC_A = rospy.get_param("~act_name_a", "selenoid_1")
	TOPIC_B = rospy.get_param("~act_name_b", "selenoid_2")
	TOPIC_C = rospy.get_param("~act_name_c", "selenoid_3")
	TOPIC_D = rospy.get_param("~act_name_d", "selenoid_4")
	topics = [TOPIC_A, TOPIC_B, TOPIC_C, TOPIC_D]

	environment = rospy.get_param("~environment_name", "astrid")
	
	setup(pines)

	createSubcribers( pines, environment, topics )

	rospy.spin()
