import paho.mqtt.client as mqtt # pip install paho.mqtt
import time
import numpy as np
import datetime




print("creating new instance")
client = mqtt.Client("PUB")
broker_address = "test.mosquitto.org" # ... use the Mosquitto test server during development


print("connecting to broker")
client.connect(broker_address)
client.loop_start()            

topic = 'teds22/group2/pressure'

#send 10 messages from publisher to broker
for _ in range(10):

    mu, sigma = 1200.00, 1.0
    reading = f'{round(np.random.normal(mu, sigma), 2):.2f}'        
    dt = datetime.datetime.now()
    dt = dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    message = f'{reading}|{dt}'
    print(f"Publishing message to topic: {topic}: {message}")
    client.publish(topic, message,qos=2) 
    time.sleep(1)

print("Publishing message 'OFF' to topic: {topic}")
client.publish(topic, "OFF")




time.sleep(4)     

print(f'Unsubscribing from topic: {topic}')
client.unsubscribe(topic) 

time.sleep(4)       
client.loop_stop()  
print("\ndisconnecting from broker")
client.disconnect()
