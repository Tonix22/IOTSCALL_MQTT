import paho.mqtt.client as mqtt
import logging
import os
import time
import json
import base64
from Parser import DataParser
from datetime import datetime

# Map of device EUI -> device name
meter_map = {
    "8CF95720000B778E": "Scall2",
    "8CF95720000B7813": "Siapa",
    "8CF95720000B8A57": "Scall3",
    "8CF95720000B8C4C": "Scall1"
}

clients = []
client_names = ["Siapa", "Scall1", "Scall2", "Scall3"]

# Set up logging
logging.basicConfig(
    filename='report.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def on_connect(client, userdata, flags, rc):
    """
    The callback for when the lora client receives a CONNACK response from the server.
    """
    if rc == 0:
        msg = f"Lora connected successfully (rc={rc}). Subscribing to all topics."
        print(msg)
        logging.info(msg)
        client.subscribe("#")  # Subscribe to all topics
    else:
        msg = f"Lora failed to connect. Return code={rc}"
        print(msg)
        logging.error(msg)

def on_disconnect(client, userdata, rc):
    """
    Called when the lora client disconnects. Attempt to reconnect.
    """
    msg = f"Lora client disconnected (rc={rc}). Attempting to reconnect..."
    print(msg)
    logging.warning(msg)
    try:
        client.reconnect()
    except Exception as e:
        logging.error(f"Reconnection attempt failed: {e}")

def on_message(client, userdata, msg):
    """
    The callback for when a PUBLISH message is received from the server.
    """
    try:
        now = datetime.now()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
        
        # Log raw payload to file (overwrite each time, if you want to append use 'a')
        with open('Payloads.log', 'w') as f:
            f.write(f"{msg.topic}:\n{formatted_date} {msg.payload}\n")

        json_obj = json.loads(msg.payload)

        device_id_field = "end_device_ids"
        device = str(json_obj[device_id_field]["device_id"]).replace('eui-', '').upper()

        if device not in meter_map:
            logging.error(f"Received message from unexpected device: {device}")
            return

        uplink_field = "uplink_message"
        if uplink_field in json_obj and "frm_payload" in json_obj[uplink_field]:
            raw_payload = json_obj[uplink_field]["frm_payload"]
        else:
            logging.error("Message missing 'uplink_message.frm_payload' field")
            logging.error(json_obj)
            logging.error("")  # Was loggin.error("") before
            return

        # Decode and parse
        hex_bytes_load = base64.b64decode(raw_payload).hex().upper()

        parser = DataParser(hex_bytes_load)
        total_current = parser.totalCurrent

        logging.info(
            f"Topic: {msg.topic}, Device: {meter_map[device]}, Current Flow: {total_current}"
        )

        # Publish to the appropriate client
        index = client_names.index(meter_map[device])
        clients[index].publish("v1/devices/me/telemetry", f'{{"flow":{total_current}}}')

    except Exception as e:
        logging.error(f"Error processing message: {e}", exc_info=True)

def setup_main_client():
    """
    Setup the main LoRa MQTT client and return it.
    """
    lora_client = mqtt.Client()
    lora_client.on_connect = on_connect
    lora_client.on_disconnect = on_disconnect
    lora_client.on_message = on_message

    # Set username and password for the main LoRa client
    lora_client.username_pw_set(
        "ifempto@scalldigital",
        "NNSXS.WA7JARTZ2POYCDLPTA6VDRMQNGKSVGFCAEBIR3Q.G5J63O2QHB4Q274CE657EYCJID6SY2CZBHYAGNYWPA5ITEJWQ5EQ"
    )

    # Connect to The Things Industries broker
    lora_client.connect("nam1.cloud.thethings.industries", 1883, 60)
    # Start the network loop in a separate thread
    lora_client.loop_start()

    return lora_client

def setup_clients():
    """
    Setup the other MQTT clients. Return a list of connected clients.
    """
    temp_clients = []
    for name in client_names:
        client = mqtt.Client(client_id=name)
        # If you need an on_connect callback for these clients, define it above
        client.username_pw_set(name, name)
        client.connect("51.222.141.106", 1883, 60)
        client.loop_start()
        temp_clients.append(client)
    return temp_clients

def main():
    logging.info("---- MQTT process started -------")
    print("Setting up main LoRa client...")
    lora_client = setup_main_client()

    print("Setting up secondary clients...")
    global clients
    clients = setup_clients()
    print("Clients started...")

    # Run indefinitely
    try:
        while True:
            time.sleep(1)  # Sleep a bit to avoid busy-wait
    except KeyboardInterrupt:
        logging.info("KeyboardInterrupt received. Shutting down gracefully.")
    except Exception as e:
        logging.error(f"Unhandled exception in main loop: {e}", exc_info=True)
    finally:
        # Stop loops before exiting
        lora_client.loop_stop()
        for c in clients:
            c.loop_stop()
        logging.info("---- MQTT process End -------")
        print("Exiting.")

if __name__ == "__main__":
    main()
