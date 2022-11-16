import paho.mqtt.client as mqtt # pip install paho.mqtt
import time
import numpy as np
import datetime




print("creating new instance")
client = mqtt.Client("P1")     # create new instance (the ID, in this case "P1", must be unique)
 # attach "on_message" callback function (event handler) to "on_message" event


#broker_address = "localhost" # Use your own MQTT Server IP Adress (or domain name) here, or ...
broker_address = "test.mosquitto.org" # ... use the Mosquitto test server during development


print("connecting to broker")
client.connect(broker_address) # connect to broker
client.loop_start()            # start the event processing loop

topic = 'teds22/group2/pressure'

#send 10 messages from publisher to broker
for _ in range(10):

    mu, sigma = 1200.00, 1.0
    reading = f'{round(np.random.normal(mu, sigma), 2):.2f}'        
    dt = datetime.datetime.now()
    dt = dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    message = f'{reading}|{dt}'
    print(f"Publishing message to topic: {topic}: {message}")
    client.publish(topic, message,qos=2) # publish
    time.sleep(1) # wait

print("Publishing message 'OFF' to topic: house/bulbs/bulb1")
client.publish("house/bulbs/bulb1", "OFF") # publish




time.sleep(4)       # wait 4 seconds before stopping the event processing loop (so all pending events are processed)



print(f'Unsubscribing from topic: {topic}')
client.unsubscribe(topic) # unsubscribe

time.sleep(4)       # wait 4 seconds before stopping the event processing loop (so all pending events are processed)
client.loop_stop()  # stop the event processing loop

print("\ndisconnecting from broker")
client.disconnect() # disconnect from broker
