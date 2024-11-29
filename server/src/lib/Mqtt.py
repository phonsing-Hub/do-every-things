import random
import json 
from paho.mqtt import client as mqtt_client

broker = '192.168.115.50'
port = 1883
topic = "64028780/Msg"
client_id = f'publish-{random.randint(0, 1000)}'

class PahoMQTT:
    def __init__(self):
        self.client = mqtt_client.Client(client_id)  # สร้าง client ใน constructor

    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print(f"Failed to connect, return code {rc}")

        self.client.on_connect = on_connect
        self.client.connect(broker, port)
        self.client.loop_start()  # เริ่ม loop

    def publish(self, data):
            json_data = json.dumps(data)
            msg = f"{json_data}"
            result = self.client.publish(topic, msg)
            status = result.rc
            if status == mqtt_client.MQTT_ERR_SUCCESS:
                print(f"Send `{msg}` to topic `{topic}`")
            else:
                print(f"Failed to send message to topic {topic}")
           

