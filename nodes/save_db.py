#!/usr/bin/python
import rospy
import time
from pymongo import MongoClient 

ENVIRONMENT_VARIABLES = create_variables(rospy.get_param('/var_types/environment_variables'))

class SaveToDB:
	def __init__(self, db_col, environment, topic, topic_type):
		self.environment = environment
		self.db_col = db_col
		self.topic = topic
		self.sub  = rospy.Subscriber(topic, topic_type, self.on_data)

	def save(self, data):
		self.db_col.update({"info.name":self.environment}, {"$push":{"records":data}})
		
	def on_data(self, item):
		timestamp = time.time()
		value = item.data
		# This is kind of a hack to correctly interpret UInt8MultiArray
		# messages. There should be a better way to do this
		if item._slot_types[item.__slots__.index('data')] == "uint8[]":
			value = [ord(x) for x in value]

		data = {"topic": self.topic,"value":value, "timestamp":timestamp}


def createSubcribers( db_col, environment ):
	# Se crean subcripciones a partir de las variables declaradas en el archivo .yaml 
	for topic_name in ENVIRONMENT_VARIABLES.itervalues():
		topic_name = str(topic_name)
		topic = "{}/measured".format(topic_name)

		SaveToDB( db_col=db_col, environment=environment, topic=topic, topic_type=Float64 )

if __name__ == '__main__':
	host = rospy.get_param("/mongodb_host")
	port = rospy.get_param("/mongodb_port")
	db = rospy.get_param("/mongodb_db", "openaggdl")
	collection = rospy.get_param("/mongodb_col", "environments")
	db_col = MongoClient(host, port)[db][collection]

	environment = rospy.get_param("~environment_name") #read_environment_from_ns(rospy.get_namespace())

	rospy.init_node("sensor_persistence")

	createSubcribers(db_col, environment)

	rospy.spin()