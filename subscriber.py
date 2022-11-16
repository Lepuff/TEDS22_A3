import paho.mqtt.client as mqtt # pip install paho.mqtt
import time
import numpy as np
import datetime
from rdflib.namespace import RDF, RDFS, XSD, SOSA, TIME
from rdflib import Namespace
from rdflib import Graph, Literal, URIRef
messages = []
messagescount = 0



# define the rdf graph
# namespaces
g = Graph()
g.bind("sosa", SOSA)
g.bind("time", TIME)
g.bind("xsd", XSD)
g.bind("rdfs", RDFS)
g.bind("rdf", RDF)

qudt = Namespace("http://qudt.org/1.1/schema/qudt#")
g.bind("qudt-1-1", qudt)
qudt_unit = Namespace("http://qudt.org/1.1/vocab/quantity#")
g.bind("qudt-unit-1-1", qudt_unit)
cdt = Namespace("http://w3id.org/lindt/custom_datatypes#")
g.bind("cdt", cdt)
base = Namespace("http://example.org/data/")
g.bind("base", base)

#types

earthAtmosphere = base['earthAtmosphere']
g.add((earthAtmosphere,RDF.type, SOSA.FeatureOfInterest))
g.add((earthAtmosphere, RDFS.label, Literal("Earth Atmosphere", lang="en")))

sensor_atmospheric_pressure = base['sensor_atmospheric_pressure']

sensor_bmp282 = base['sensor_bmp282']
g.add((sensor_bmp282, RDF.type, SOSA.Sensor))
g.add((sensor_bmp282, RDFS.label, Literal("Bosch Sensortec BMP282", lang="en")))
g.add((sensor_bmp282,SOSA.observes,sensor_atmospheric_pressure))

iphone = base['iphone']
g.add((iphone, RDF.type ,SOSA.Platform))
g.add((iphone, RDFS.label,Literal("iPhone", lang="en")))
g.add((iphone,RDFS.comment,Literal("Apple iPhone 7", lang="en")))
g.add((iphone, SOSA.hosts, sensor_bmp282))




print("creating new instance")
client = mqtt.Client("P2")     # create new instance (the ID, in this case "P1", must be unique)

def on_message(client, userdata, message):
    
    global messages
    global messagescount
    print(f"\nmessage payload: {message.payload.decode('utf-8')}")
    print(f"message topic: {message.topic}")
    print(f"message qos: {message.qos}")
    print(f"message retain flag: {message.retain}")
    #split the message
    message = message.payload.decode('utf-8')
    [value,  timestamp] = message.split('|')
  

    #add to the rdf graph
    #observation

    observation = base['Observation/' + str(messagescount)]
    g.add((observation, RDF.type, SOSA.Observation))
    g.add((observation, SOSA.observedProperty, sensor_bmp282))
    g.add((observation, SOSA.hasFeatureOfInterest, earthAtmosphere))
    g.add((observation, SOSA.madeBySensor, sensor_bmp282))
    g.add((observation,SOSA.hasSimpleResult,Literal(value, datatype=cdt.Pascal)))
    g.add((observation, SOSA.resultTime, Literal(timestamp, datatype=XSD.dateTime)))
    messages.append(message)
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


#save the rdf graph
g.serialize(destination='pressure.ttl')
