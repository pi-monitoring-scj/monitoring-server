import paho.mqtt.client as mqtt
from fastapi import FastAPI, WebSocket
import json
import asyncio
import os
import time

app = FastAPI()
latest_data = {}

MQTT_HOST = os.getenv("MQTT_BROKER_HOST", "localhost")

def on_message(client, userdata, msg):
    global latest_data
    try:
        latest_data = json.loads(msg.payload.decode())
    except Exception as e:
        print(f"Error decoding message: {e}")

# paho-mqtt 2.0 이상 버전 대응 (CallbackAPIVersion 설정)
try:
    mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
except AttributeError:
    mqtt_client = mqtt.Client() # 구버전일 경우

mqtt_client.on_message = on_message

# 브로커가 켜질 때까지 재시도하는 로직
connected = False
while not connected:
    try:
        print(f"Connecting to MQTT Broker at {MQTT_HOST}...")
        mqtt_client.connect(MQTT_HOST, 1883)
        connected = True
    except Exception as e:
        print(f"Failed to connect to MQTT, retrying in 2s... ({e})")
        time.sleep(2)

mqtt_client.subscribe("sensor/mpu6050/raw")
mqtt_client.loop_start()

@app.get("/")
def read_root():
    return {"status": "online", "latest_sensor_data": latest_data}

@app.websocket("/ws/sensor")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await websocket.send_json(latest_data)
            await asyncio.sleep(0.1)
    except Exception:
        await websocket.close()