import paho.mqtt.client as mqtt
import logging
import os
import time
import json
import base64
from Parser import DataParser
from datetime import datetime

meter_map ={"8CF95720000B778E": "Scall2",
            "8CF95720000B7813": "Siapa",
            "8CF95720000B8A57": "Scall3",
            "8CF95720000B8C4C": "Scall1"}

clients = []
client_names = ["Siapa", "Scall1", "Scall2", "Scall3"]


# Set up logging
logging.basicConfig(filename='report.log', filemode='a', 
                    format='%(asctime)s - %(message)s', level=logging.INFO)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print(f"Lora connected with result {str(rc)}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("#") # Subscribe to all topics
    
def on_serverconnect(client, userdata, flags, rc):
    print(f"Connected with result code {str(rc)}")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    
    print(msg.topic+": \n"+formatted_date+" "+str(msg.payload), file=open('Payloads.log', 'w'))

    json_obj = json.loads(msg.payload)
    
    device_id_field = "end_device_ids"  # <-- This was the typo.

    device = str(json_obj[device_id_field]["device_id"]).replace('eui-', '').upper()
    
    if device not in meter_map:
        logging.error(f"Received message from unexpected device: {device}")
        return

    uplink_field = "uplink_message"
    if uplink_field in json_obj and "frm_payload" in json_obj[uplink_field]:
        raw_payload = json_obj[uplink_field]["frm_payload"]
    else:
        logging.error("Message didn't contain expected 'uplink_message.frm_payload' field")
        logging.error(json_obj)
        loggin.error("")
        return

    raw_payload = json_obj[uplink_field]["frm_payload"]
    hex_bytes_load = base64.b64decode(raw_payload).hex().upper()

    try:
        parser = DataParser(hex_bytes_load)
    except Exception as e:
        logging.error(f"Failed to parse payload: {e}")
        return

    total_current = parser.totalCurrent

    logging.info(f"Topic: {msg.topic}, Message: Device: {meter_map[device]}, Current Flow: {total_current}")
    
    index = client_names.index(meter_map[device])

    clients[index].publish("v1/devices/me/telemetry", f'{{"flow":{total_current}}}')
    
logging.info("---- MQTT process started -------")

lora   = mqtt.Client()
#handlers
lora.on_connect = on_connect
lora.on_message = on_message
# Set username and password for the second client
lora.username_pw_set("ifempto@scalldigital", "NNSXS.WA7JARTZ2POYCDLPTA6VDRMQNGKSVGFCAEBIR3Q.G5J63O2QHB4Q274CE657EYCJID6SY2CZBHYAGNYWPA5ITEJWQ5EQ")  
# Connect to the broker - replace 'localhost' and 1883 with your broker's IP and port
lora.connect("nam1.cloud.thethings.industries", 1883, 60)



for name in client_names:
    client = mqtt.Client(client_id=name)
    #client.on_connect = on_serverconnect
    client.username_pw_set(name, name)
    client.connect("51.222.141.106", 1883, 60)
    client.loop_start()
    clients.append(client)

print("clients started ...")
# loop
lora.loop_start()

# Define the duration in seconds (1 days = 1 * 24 * 60 * 60 seconds)
duration_seconds = 24 * 60 * 60

# Get the current time
start_time = time.time()

while (time.time() - start_time) < duration_seconds:
    pass

logging.info("---- MQTT process End -------")