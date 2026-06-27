# Day 1: MQTT Pub/Sub Architecture Setup and Sensor Simulation 🚀

This project was developed as part of the **Day 1** backend infrastructure preparation process for Industrial IoT (IIoT) and Predictive Maintenance systems. 

In this phase, a simple Publisher/Subscriber architecture was established using the **MQTT (Message Queuing Telemetry Transport)** protocol to listen to data from industrial sensors in real-time with low latency.

## 📌 What We Did
* Grasped the working logic (Pub/Sub) of the MQTT protocol, which is the communication standard for IoT devices.
* Instead of writing a broker from scratch on our local machine, we connected to a ready-to-use, industry-standard public broker (`broker.emqx.io`).
* Wrote two different Python services using the `paho-mqtt` library:
  1. **Publisher (`sensor.py`):** Simulates a temperature sensor of a motor in a factory. It generates random temperature data and publishes it to a specific MQTT topic.
  2. **Subscriber (`listener.py`):** Simulates the backend service. It subscribes to the relevant topic, listens to the incoming data from the sensor in real-time, and prints it to the terminal.

## 🛠️ Technologies Used
* **Language:** Python 3.x
* **Library:** `paho-mqtt`
* **Broker:** EMQX Public Test Broker (`broker.emqx.io` - Port: 1883)
* **Environment:** Python Virtual Environment (`venv`)

## 🚀 Setup and Execution

It is highly recommended to use a virtual environment to isolate the project dependencies.

**1. Create and activate the virtual environment:**
```bash
python -m venv venv

# For Windows (PowerShell):
.\venv\Scripts\activate

# For Linux/macOS:
source venv/bin/activate
```

**2. Install the required library:**
```bash
pip install paho-mqtt
```

3. Run the System:
   Open two different terminal windows (ensure the virtual environment is active in both).
   In the first terminal, run the subscriber (backend simulation):

```bash
python dinleyici.py
```

In the second terminal, run the sensor (data producer):
```bash
python sensor.py
```



Expected Output
As soon as the sensor script runs, it starts publishing data to the factory/room/test topic.
You should see a real-time stream in the subscriber terminal similar to this:

```bash
YENİ VERİ GELDİ -> Konu: factory/room/test | Mesaj: Motor Sicakligi: 24.1 C
YENİ VERİ GELDİ -> Konu: factory/room/test | Mesaj: Motor Sicakligi: 26.93 C
```


## Day 2: Data Persistence and InfluxDB Integration 🗄️

As part of the second day, **InfluxDB**, a Time Series Database (TSDB), was integrated into the system to enable historical analysis of real-time streaming data (establishing the foundation for predictive maintenance).

**Improvements Made:**
* **Transition to JSON Format:** Sensor data (temperature and humidity) was converted from plain text to the industry-standard JSON format, making it easier to parse and process.
* **QoS 1 (Quality of Service):** To prevent data loss during network interruptions, the MQTT communication level was upgraded to QoS 1 ("At least once" delivery guarantee).
* **InfluxDB Docker Setup:** Instead of installing it on the local machine, InfluxDB was spun up as an isolated Docker container.
* **Python - InfluxDB Bridge:** The `influxdb-client` was integrated into the `dinleyici.py` service, ensuring that data captured from MQTT is written to the InfluxDB 'sensor_verileri' bucket in real-time.

**Technologies Used:** InfluxDB 2.7, Docker, Python `influxdb-client`, JSON
