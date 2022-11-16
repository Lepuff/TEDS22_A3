import paho.mqtt.client as mqtt # pip install paho.mqtt
import time
import numpy as np
import datetime
from rdflib.namespace import RDF, RDFS, XSD, SOSA, TIME
from rdflib import Namespace
messages = []
messagescount = 0



# define the rdf graph




""""
@prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix sosa: <http://www.w3.org/ns/sosa/> .
@prefix time: <http://www.w3.org/2006/time#>.
@prefix qudt-1-1: <http://qudt.org/1.1/schema/qudt#> .
@prefix qudt-unit-1-1: <http://qudt.org/1.1/vocab/unit#> .
@prefix cdt: <http://w3id.org/lindt/custom_datatypes#> .
@base <http://example.org/data/> .

# The barometric readings from a Bosch Sensortec BMP282 sensor in an Apple IPhone 7
# observed on June 6 2017 using only the SOSA core for modelling.

<earthAtmosphere> rdf:type sosa:FeatureOfInterest ;
  rdfs:label "Atmosphere of Earth"@en .


# An iPhone 7 as the Platform that hosts several sensors,
# among others the Bosch Sensortec BMP282 atmospheric pressure sensor.

<iphone7/35-207306-844818-0> a sosa:Platform ;
  rdfs:label "IPhone 7 - IMEI 35-207306-844818-0"@en ;
  rdfs:comment "IPhone 7 - IMEI 35-207306-844818-0 - John Doe"@en ;
  sosa:hosts <sensor/35-207306-844818-0/BMP282> .

<sensor/35-207306-844818-0/BMP282> rdf:type sosa:Sensor ;
  rdfs:label "Bosch Sensortec BMP282"@en ;
  sosa:observes <sensor/35-207306-844818-0/BMP282/atmosphericPressure> .
"""

print("creating new instance")
client = mqtt.Client("P2")     # create new instance (the ID, in this case "P1", must be unique)

def on_message(client, userdata, message):
    
    global messages
    global messagescount
    print(f"\nmessage payload: {message.payload.decode('utf-8')}")
    print(f"message topic: {message.topic}")
    print(f"message qos: {message.qos}")
    print(f"message retain flag: {message.retain}")
    messages.append(message.payload.decode('utf-8'))
    messagescount += 1
    time.sleep(1)
client.on_message = on_message # attach "on_message" callback function (event handler) to "on_message" event


#broker_address = "localhost" # Use your own MQTT Server IP Adress (or domain name) here, or ...
broker_address = "test.mosquitto.org" # ... use the Mosquitto test server during development
topic = 'teds22/group2/pressure'

print("connecting to broker")
client.connect(broker_address) # connect to broker
client.subscribe(topic) # subscribe
client.loop_start()            # start the event processing loop
# Create an "on_message" callback function (event handler) for the "on_message" event


# wait for 10 messages


while messagescount < 10:
    pass

# unsubscribe from topic
print("Unsubscribing from topic: {topic}")
client.unsubscribe(topic) # unsubscribe
client.loop_stop()  # stop the event processing loop

#disconnect from broker
print("\ndisconnecting from broker")
client.disconnect() # disconnect from broker
