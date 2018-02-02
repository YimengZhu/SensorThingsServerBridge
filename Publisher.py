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


'''
If run this script, it will periodlly publish all entities via MQTT
'''
if __name__ == '__main__':
	
	counter = 0

	location_id = 2
	thing_id = 2
	sensor_id = 2
	observedProperty_id = 2
	datastream_id = 2
	foi_id = 2
	observation_id = 2

	# loop
	while True:

		# post a location
		location = Location('location ' + str(counter) , 'location ' + str(counter) , 
			Feature(geometry = Point((counter, counter))))
		publish.single('v1.0/Locations', location.jsonSerialize()) 

		# post a thing 
		thing = Thing('thing ' + str(counter), 'thing ' + str(counter))
		publish.single('v1.0/Things', thing.jsonSerialize()) 

		# post a sensor
		sensor = Sensor("sensor " + str(counter) , "sensor " + str(counter))
		publish.single('v1.0/Sensors', sensor.jsonSerialize()) 

		# post a Observed Property
		observedProperty =  {
			"name" : 'observedProperty ' + str(counter),
			"definition" : 'observedProperty ' + str(counter),
			"description" : 'observedProperty ' + str(counter),
		}
		publish.single('v1.0/ObservedProperties', json.dumps(observedProperty)) 

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
		publish.single('v1.0/Datastreams', json.dumps(datastream)) 


		# post a foi
		foiFeature = {
			"type" : "Feature",
			"geometry" : {
				"type" : "Point",
				"coordinates" : [0, 0]
			}
		}
		foi = FeaturesOfInterest('foi ' + str(counter), 'foi ' + str(counter), 'application.geo+json', foiFeature)
		publish.single('v1.0/FeaturesOfInterests', foi.jsonSerialize()) 


		# publish a observation
		timestamp = datetime.datetime.now().isoformat()
		observation = Observation(timestamp, counter, timestamp, {"@iot.id" : datastream_id}, {"@iot.id" : foi_id})
		publish.single('v1.0/Observations', observation.jsonSerialize()) 
		
		counter += 1
		time.sleep(3)


