#!/usr/bin/python
import rospy
from std_msgs.msg import Float64
import os
import paho.mqtt.client as client#Indica que sera un cliente mqtt y solo recibira informacion
import paho.mqtt.publish as publish#indica que se utilizara como Broker y que enviara mensajes
import netifaces as ni # para consultar ip address
from libs.load_env_var_types import create_variables

BASE_TOPIC_BRKR = ["/broker/bd/#","/broker/broadcast/#" ]
BASE_TOPIC_CLI = "/environment/astrid/{}" # /environment/ENVIRONMENT_NAME/VAR_SUBJECT
IP = "0.0.0.0"
ENVIRONMENT_VARIABLES = create_variables(rospy.get_param('/var_types/environment_variables')) 
#ENVIRONMENTS = ["astrid"]


class ClientMQTT:
    """docstring for ClientMQTT"""
    #@param HOST
    #@param PORT
    #@param KEEPALIVE
    def __init__(self, host="0.0.0.0", port=1883, keepalive=60):
        self.host = host
        self.port = port
        self.keepalive = keepalive
        #self.topics = topics
        self.setup()

    def on_connect(self, client, userdata, flags, rc):
        rospy.loginfo("Connected with result code {}".format(rc))#indica el ID de conexion, un resultado 0 es optimo
        
        #for variable in ENVIRONMENT_VARIABLES.itervalues():
        topic = BASE_TOPIC_CLI.format("#") # # hashtag equivale a * comodin
        client.subscribe(topic)#indica al topico que se va a suscribir
        rospy.loginfo("client MQTT subscribed to : {}".format(topic))

        client.subscribe("/broker/broadcast/#")
        rospy.loginfo("client MQTT subscribed to : /broker/broadcast/#")

    def on_message(self, client, userdata, msg):#Actividad que realizara cada vez que recibe un mensaje
        rospy.logwarn("We got a message")
        rospy.logwarn("{} {}".format(msg.topic, msg.payload))#imprime el topico de donde vino y el mensaje importo paho.mqtt.client as mqtt

    def publish(self, msg):
        self.publish(self.topic, msg)

    def setup(self):
        self.client = client.Client()#Crea el cliente mqtt
        self.client.on_connect = self.on_connect # Metodo que crea la conexion con el broker
        self.client.on_message = self.on_message # Metodo que recibe los mensajes            
        self.client.connect(self.host, self.port, self.keepalive)#Ejecuta la conexion con el Broker, la direccion ip pertenece al broker
        self.client.loop_forever()#Ejecuta de forma ciclica todas las funciones de paho-mqtt

class PublishMQTT(object):
    """docstring for PublishMQTT"""
    def __init__(self, host, topic, topic_type):
        self.host = host
        self.topic = topic
        self.topic_type = topic_type
        self.sub  = rospy.Subscriber(self.topic, self.topic_type, self.on_data)

    def cast(self, msg):
        CMD = "mosquitto_pub -h {} -t '{}' -m {}".format(self.host, self.topic, msg)
        os.system(CMD)
    
    def on_data(self, item):
        timestamp = time.time()
        value = item.data
        # This is kind of a hack to correctly interpret UInt8MultiArray
        # messages. There should be a better way to do this
        if item._slot_types[item.__slots__.index('data')] == "uint8[]":
            value = [ord(x) for x in value]

        msg = {"topic": self.topic,"value":value, "timestamp":timestamp}
        self.cast(msg)
        

class BrokerMQTT:
   #docstring for BrokerMQTT
    def __init__(self, host):
        self.host = host

       
    def createSubcribers( db_col, environment ):
        # Se crean subcripciones a partir de las variables declaradas en el archivo .yaml 
        for topic_name in ENVIRONMENT_VARIABLES.itervalues():
            topic_name = str(topic_name)
            topic = "{}/raw".format(topic_name) #de manera formal se deberia guardar del topico */measure

            PublishMQTT( self.host, topic=topic, topic_type=Float64 )
       
def setupMQTT(host, is_broker):
    if is_broker:
        BrokerMQTT(host=host)
    else:
        ClientMQTT(host=host)

def myIp():
    return ni.ifaddresses('eth0')[ni.AF_INET][0]['addr'] # should print "192.168.100.37"

def brokerMQTT():
    #TODO: scanear la red y preguntar por el broker
    #TODO: si no hay broker asignar al de ip mas chica
    return rospy.get_param("~broker_ip", "0.0.0.0")

def updateEnvironmentsList():
    #TODO: validar que los ambientes conectados a la red
    #TODO: actualizar array ENVIRONMENTS
    pass

if __name__ == '__main__':
    rospy.init_node("community")
    
    HOST_BROKER = brokerMQTT()
    IP = myIp()
    #TOPICS = [ "test_topic" ]
    is_broker = True if (HOST_BROKER == "0.0.0.0") | (HOST_BROKER == IP) else False

    setupMQTT(HOST_BROKER, is_broker)


    rospy.spin()
