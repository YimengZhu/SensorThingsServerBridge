from Utils import *
import paho.mqtt.client as mqtt 
import paho.mqtt.publish as publish
import json

def read_config():
	pass

def on_connect(client, userdata, flags, rc):
	client.subscribe('v1.0/Things')
	client.subscribe('v1.0/Sensors')
	client.subscribe('v1.0/Locations')
	client.subscribe('v1.0/ObservedProperties')
	client.subscribe('v1.0/Datastreams')
	client.subscribe('v1.0/FeaturesOfInterest')

def on_message(client, userdata, msg):
	topic = msg.topic.split('/')[-1]

	valid_topics = ['Datastreams', 'FeaturesOfInterest', 'ObservedProperties', 'Locations', 'Sensors', 'Things']
	if topic in valid_topics:
		json_dict = json.loads(msg.payload.decode("utf-8"))
		
		# check if this message is generated from SensorThings Server
		for k, v in json_dict.items():
			if "@iot.navigation" in k:
				return
			if  "@iot.selflink" in k:
				pass

		print(json.dumps(json_dict))
		print(topic)

		create_via_rest(json.dumps(json_dict), topic)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)
client.loop_forever()    