import paho.mqtt.client as mqtt # pip install paho.mqtt
import time
import numpy as np
import datetime
from rdflib.namespace import RDF, RDFS, XSD, SOSA, TIME

messages = []
messagescount = 0






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
