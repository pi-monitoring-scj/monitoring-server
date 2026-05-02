# Monitoring-Server (Phase 1)
> **Centralized Data Hub for Real-time Sensor Telemetry**  
> 라즈베리 파이로부터 수집된 물리 데이터를 통합 관리하고 실시간 시각화를 위한 데이터를 스트리밍하는 백엔드 서버입니다.

##  Project Role
이 서버는 전체 모니터링 시스템의 **'관제 센터(Control Center)'** 역할을 수행합니다.
* **MQTT Subscriber**: 라즈베리 파이(Mosquitto Broker)에 접속하여 실시간 센서 데이터를 수집합니다.
* **WebSocket Provider**: 수집된 데이터를 웹 프론트엔드(React)가 실시간으로 렌더링할 수 있도록 고속 스트리밍 통로를 제공합니다.
* **Data Processor**: 로우 데이터를 가공하여 상위 애플리리케이션에서 사용하기 적합한 형태로 변환합니다.

---

##  Tech Stack
* **Language**: Python 3.10+
* **Framework**: FastAPI
* **Communication**: 
    * **MQTT**: Paho-MQTT (Internal Communication)
    * **WebSocket**: Fast-API WebSockets (External Streaming)
* **Environment**: macOS (Development / Control Center)

---

##  Data Flow
1. **MQTT Subscribe**: `sensor/mpu6050` 토픽을 통해 라즈베리 파이의 데이터를 수신.
2. **Buffering**: 수신된 최신 데이터를 메모리에 유지(Caching).
3. **Broadcasting**: WebSocket을 통해 연결된 모든 웹 클라이언트에 JSON 형태로 전송.

---
