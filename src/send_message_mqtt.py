import paho.mqtt.client as mqtt 
from dataclasses import dataclass, asdict
import json
import os

mqttBroker = os.environ.get('MQTT_HOST', "localhost")

@dataclass
class TyreMessage:
    """Class for keeping track of an item in inventory."""
    number: int
    name: str
    psi: float
    temp: float
    battery: int
    warning: bool
    sensor_id: str


def send_message(message: TyreMessage):
    client = mqtt.Client("Temperature_Inside")
    client.connect(mqttBroker) 
    client.publish(f"TYRE_{message.number}", json.dumps(asdict(message)) )