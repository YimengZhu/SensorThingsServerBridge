import json
import urllib
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import re
import paho.mqtt.client as mqtt 
import paho.mqtt.publish as publish
from Entity import *
from geojson import Point, Feature
import datetime
import time


# get id from the server response
def get_id_from_response(res):
	lastPart = res.split('/')[-1]
	idInResponse = int(re.search(r'\d+', lastPart).group())
	return idInResponse

# get current 

# create an entity via the REST API
def create_via_rest(data, urltail):
	url = 'http://localhost:8080/SensorThingsService/v1.0/' + urltail
	payload = data.encode('ascii')
	req = Request(url, payload, {'Content-Type': 'application/json'})
	f = urlopen(req)
	responseHeader = f.getheader('location')
	f.close()
	return responseHeader

# Create an Observation via MQTT broker
def create_via_mqtt(observation):
	publish.single('v1.0/Observations', observation.jsonSerialize())



'''
If run this script, it will periodlly post entities other than observation via REST API and 
Observation via MQTT
'''
if __name__ == '__main__':
	
	counter = 0

	location_id = None
	thing_id = None
	sensor_id = None
	observedProperty_id = None
	datastream_id = None
	foi_id = None
	observation_id = None

	# loop
	while True:

		# post a location
		location = Location('location ' + str(counter) , 'location ' + str(counter) , 
			Feature(geometry = Point((counter, counter))))
		location_res = create_via_rest(location.jsonSerialize(), 'Locations')
		location_id = get_id_from_response(location_res)

		# post a thing 
		thing = Thing('thing ' + str(counter), 'thing ' + str(counter))
		thing_res = create_via_rest(thing.jsonSerialize(), 'Things')
		thing_id = get_id_from_response(thing_res)

		# post a sensor
		sensor = Sensor("sensor " + str(counter) , "sensor " + str(counter))
		sensor_res = create_via_rest(sensor.jsonSerialize(), 'Sensors')
		sensor_id = get_id_from_response(sensor_res)

		# post a Observed Property
		observedProperty =  {
			"name" : 'observedProperty ' + str(counter),
			"definition" : 'observedProperty ' + str(counter),
			"description" : 'observedProperty ' + str(counter),
		}
		observedProperty_res = create_via_rest(json.dumps(observedProperty), 'ObservedProperties')
		observedProperty_id = get_id_from_response(observedProperty_res)

		# post a datastream
		datastream =  {
			"name" : "Datastream " + str(counter),
			"description" : "Datastream " + str(counter),
			"unitOfMeasurement" : {	"name" : "unitOfMeasurement " + str(counter),
	 								"symbol" : "mm",
	 								"definition" : "sdfasd"
								},
			"observationType" : "Datastream " + str(counter),
			"Thing" : { "@iot.id" : thing_id},
			"Sensor" : { "@iot.id" : sensor_id},
			"ObservedProperty" : {"@iot.id" : observedProperty_id}
		}
		datastream_res = create_via_rest(json.dumps(datastream), 'Datastreams')
		datastream_id = get_id_from_response(datastream_res)

		# post a foi
		foiFeature = {
			"type" : "Feature",
			"geometry" : {
				"type" : "Point",
				"coordinates" : [0, 0]
			}
		}
		foi = FeaturesOfInterest('foi ' + str(counter), 'foi ' + str(counter), 'application.geo+json', foiFeature)
		foi_res = create_via_rest(foi.jsonSerialize(), 'FeaturesOfInterest')
		foi_id = get_id_from_response(foi_res)

		# publish a observation
		timestamp = datetime.datetime.now().isoformat()
		observation = Observation(timestamp, counter, timestamp, {"@iot.id" : datastream_id}, {"@iot.id" : foi_id})
		publish.single('v1.0/Observations', observation.jsonSerialize()) 
		
		counter += 1
		time.sleep(3)


