import paho.mqtt.client as mqtt
import json
import time
import random
import os

# 도커 네트워크 안에서는 서비스 이름인 'mosquitto'로 접근합니다.
MQTT_HOST = os.getenv("MQTT_HOST", "mosquitto")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client.connect(MQTT_HOST, 1883)

print(f"Connecting to {MQTT_HOST} and sending fake data...")

try:
    while True:
        fake_data = {
            "accel_x": round(random.uniform(-1.0, 1.0), 3),
            "accel_y": round(random.uniform(-1.0, 1.0), 3),
            "accel_z": round(random.uniform(9.0, 10.0), 3),
            "gyro_x": random.randint(-10, 10)
        }
        client.publish("sensor/mpu6050", json.dumps(fake_data))
        time.sleep(1)
except KeyboardInterrupt:
    pass