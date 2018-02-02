from Utils import *
import paho.mqtt.client as mqtt 
import paho.mqtt.publish as publish
import json

master_server = 'localhost'
slave_server = '192.168.0.87'

plural_singular = {'Things':'Thing', 'Sensors':'Sensor', 'Locations':'Location', 
	'Observations':'Observation', 'ObservedProperties':'ObservedProperty', 
	'Datastreams':'Datastream', 'FeaturesOfInterests':'FeaturesOfInterest',
	'HistoricalLocations':'HistoricalLocation'}


def read_config():
	pass


def parse_payload(payload):

	json_dict = json.loads(payload)

	for k,v in json_dict.copy().items():
		if "@iot.self" in k:
			json_dict.pop(k)
		if "@iot.id" in k:
			json_dict.pop(k)
		if "@iot.navigation" in k:
			if k.split('@')[0] in plural_singular:
				new_k = plural_singular[k.split('@')[0]]
			else:
				continue
			iot_id = int(v.split('/')[-2].split('(')[-1][:-1])
			new_v = {'iot.id':iot_id}
			json_dict.pop(k)
			json_dict[new_k] = new_v

	json_string = json.dumps(json_dict)

	return json_string


def on_connect(client, userdata, flags, rc):
	client.subscribe('v1.0/Things')
	client.subscribe('v1.0/Sensors')
	client.subscribe('v1.0/Locations')
	client.subscribe('v1.0/ObservedProperties')
	client.subscribe('v1.0/Datastreams')
	client.subscribe('v1.0/FeaturesOfInterest')
	client.subscribe('v1.0/Observations')

def on_message(client, userdata, msg):
	topic = msg.topic.split('/')[-1]
	payload = msg.payload.decode("utf-8")

	payload = parse_payload(payload)
	print(topic)
	print(payload)
	print('=========================')

	if topic == 'v1.0/Observations':
		publish.single('v1.0/Observations', payload, host = slave_server)
	
	elif topic in ['Datastreams', 'FeaturesOfInterest', 'ObservedProperties', 'Locations', 'Sensors', 'Things']:
		create_via_rest(payload, topic, server_path = slave_server + ':8080/SensorThingsServer-1.0')

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)
client.loop_forever()    