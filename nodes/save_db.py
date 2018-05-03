#!/usr/bin/python
"""Nodo usado como local storageclear"""
import rospy
import time
from std_msgs.msg import Float64
from pymongo import MongoClient
from urllib import quote_plus
from libs.load_env_var_types import create_variables

ENVIRONMENT_VARIABLES = create_variables(rospy.get_param('/var_types/environment_variables'))

class SaveToDB:
	"""docstring for SaveToDB"""
	def __init__(self, db_col, environment):
		self.db_col = db_col
		self.environment = environment

	def save(self, data):
		try:
			self.db_col.insert(data)
		except Error:
			rospy.logwarn("Error al intentar guardar datos en la base : {}".format(Error))
		

class SubscriberToDB:
	def __init__(self, db_col, environment, topic, topic_type):
		self.environment = environment
		self.db_col = db_col
		self.topic = topic
		self.sub  = rospy.Subscriber(topic, topic_type, self.on_data)
		

	def save(self, data):
		try:
			SaveToDB(self.db_col, self.environment).save(data)
		except Error:
			rospy.logwarn("Error al intentar guardar datos en la base : {}".format(Error))
		
	def on_data(self, item):
		timestamp = time.time()
		value = item.data
		# This is kind of a hack to correctly interpret UInt8MultiArray
		# messages. There should be a better way to do this
		if item._slot_types[item.__slots__.index('data')] == "uint8[]":
			value = [ord(x) for x in value]

		data = {"topic": self.topic,"value":value, "timestamp":timestamp}
		self.save(data)


def createSubcribers( db_col, environment ):
	# Se crean subcripciones a partir de las variables declaradas en el archivo .yaml 
	for topic_name in ENVIRONMENT_VARIABLES.itervalues():
		topic_name = str(topic_name)
		topic = "{}/raw".format(topic_name) #de manera formal se deberia guardar del topico */measure

		SubscriberToDB( db_col=db_col, environment=environment, topic=topic, topic_type=Float64 )

if __name__ == '__main__':
	host = rospy.get_param("~mongodb_host", "localhost")
	port = rospy.get_param("~mongodb_port", 27017)
	user = rospy.get_param("~mongodb_user")
	pwd = rospy.get_param("~mongodb_pwd")
	db = rospy.get_param("~mongodb_db", "openaggdl")
	collection = rospy.get_param("~mongodb_col", "records") # coleccion donde se guardan los datos recibidos
	
	uri = "mongodb://{}:{}@{}:{}/{}".format(quote_plus(user), quote_plus(pwd), quote_plus(host), quote_plus(port), quote_plus(db))
	db_col = MongoClient(uri)[db][collection]

	environment = rospy.get_param("~environment_name", "astrid") #read_environment_from_ns(rospy.get_namespace())

	rospy.init_node("sensor_persistence")

	createSubcribers(db_col, environment)

	rospy.spin()
