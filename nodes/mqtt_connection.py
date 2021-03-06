#!/usr/bin/python
import rospy
from std_msgs.msg import Float64
import time
import paho.mqtt.client as client#Indica que sera un cliente mqtt y solo recibira informacion
import paho.mqtt.publish as publish#indica que se utilizara como Broker y que enviara mensajes
import netifaces as ni # para consultar ip address
from libs.load_env_var_types import create_variables

BASE_TOPIC_BRKR = ["/broker/bd/#","/broker/broadcast/#" ]
BASE_TOPIC_CLI = "/environments/{}/{}" # /environment/ENVIRONMENT_NAME/VAR_SUBJECT
ENVIRONMENT = "astrid"
IP = "0.0.0.0"
ENVIRONMENT_VARIABLES = create_variables(rospy.get_param('/var_types/environment_variables')) 
IS_BROKER = False
#ENVIRONMENTS = ["astrid"]

class ROSSubscriber:
    """docstring for ROSSubscriber"""
    def __init__(self, mqtt, topic="", topic_type=Float64):
        self.mqtt = mqtt #instancia creada de mqtt
        self.topic = topic # topic for ROS
        self.topic_type = topic_type # type_topic for ROS
        # subcribe to topic ROS
        self.sub  = rospy.Subscriber(self.topic, self.topic_type, self.on_data)

    def on_data(self, item):
        # function on event from ROS
        timestamp = time.time()
        value = item.data
        # This is kind of a hack to correctly interpret UInt8MultiArray
        # messages. There should be a better way to do this
        if item._slot_types[item.__slots__.index('data')] == "uint8[]":
            value = [ord(x) for x in value]

        msg = {"environment":ENVIRONMENT,"topic": self.topic,"value":value, "timestamp":timestamp}
        topic_save = BASE_TOPIC_CLI.format(ENVIRONMENT, "save")
        self.mqtt.publisher(str(topic_save), msg)
        

class SetupMQTT:
    """docstring for SetupMQTT"""
    def __init__(self, host="0.0.0.0", port=1883, keepalive=60):
        self.host = host
        self.port = port
        self.keepalive = keepalive
        self.setup_MQTT()

    def setup_MQTT(self):
        # Setup MQTT Client
        self.client = client.Client()#Crea el cliente mqtt
        self.client.on_connect = self.on_connect # Metodo que crea la conexion con el broker
        self.client.on_message = self.on_message # Metodo que recibe los mensajes            
        self.client.connect(self.host, self.port, self.keepalive)#Ejecuta la conexion con el Broker, la direccion ip pertenece al broker
        self.client.loop_start()#inicia un hilo que se conecta con el broker

    def on_connect(self, client, userdata, flags, rc):
        # subscribe to MQTT channels 
        rospy.logwarn("Connected with result code {}".format(rc))#indica el ID de conexion, un resultado 0 es optimo
        # Se subscribe a los canales MQTT particulares del ambiente
        topic = BASE_TOPIC_CLI.format(ENVIRONMENT, "#") # /environment/ENVIRONMENT_NAME/VAR_SUBJEC/# hashtag equivale a * comodin
        client.subscribe(topic)#indica al topico que se va a suscribir
        rospy.logwarn("client MQTT subscribed to : {}".format(topic))

        # - Se subscribe al canal MQTT general del broker 
        client.subscribe("/broker/broadcast/#")
        rospy.logwarn("client MQTT subscribed to : /broker/broadcast/#")

    def on_message(self, client, userdata, msg):#Actividad que realizara cada vez que recibe un mensaje
        rospy.logdebug("on_message: We got a message")
        rospy.logdebug("{} {}".format(msg.topic, msg.payload))#imprime el topico de donde vino y el mensaje importo paho.mqtt.client as mqtt
        self.cast(str(self.filterTopic(msg.topic)), str(msg.payload))

    def filterTopic(self, fromTopic):
        topic = fromTopic
        
        if ("save" in fromTopic) & IS_BROKER:
            topic = "/broker/db/save"

        return topic

    def publisher(self, topic, msg):
        # publica MQTT en modo cliente
        topic = self.filterTopic(topic) # filtra el topico si es broker
        rospy.logdebug("PUBLISH TO mqtt:{} THIS : {}".format(topic, msg))
        self.client.publish(str(topic), str(msg))

    def cast(self,topic="/broker/broadcast/cmd", msg=""):
        #publica MQTT en modo Broker
        # TODO: publica mensages en el topico general
        publish.single(str(topic), str(msg))

        

def createROSSubcribers( host ):
    
    MQTT = SetupMQTT( host=host ) # se crea una instancia para mqtt
    
    # Se crean subcripciones a partir de las variables declaradas en el archivo .yaml 
    for topic_name in ENVIRONMENT_VARIABLES.itervalues():
        topic_name = str(topic_name)
        topic = "{}/raw".format(topic_name) #de manera formal se deberia guardar del topico */measure

        ROSSubscriber( mqtt=MQTT, topic=topic, topic_type=Float64 )
       
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
    ENVIRONMENT = rospy.get_param("~environment_name", "astrid")
    HOST_BROKER = brokerMQTT() # obtiene la direccion del broker
    IP = myIp() 
    IS_BROKER = True if (HOST_BROKER == "0.0.0.0") | (HOST_BROKER == IP) else False

    createROSSubcribers(HOST_BROKER)

    rospy.spin()
