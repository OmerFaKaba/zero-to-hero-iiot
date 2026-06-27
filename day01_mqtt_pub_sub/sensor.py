import paho.mqtt.client as mqtt
import time
import random
import json

# MQTT istemcisini oluşturuyoruz 
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# Test Broker'ına bağlanıyoruz
client.connect("broker.emqx.io",1883,60)

print("Sensör JSON formatında veri göndermeye başaldı (QoS 1)...")

try: 
    while True:
        # Rastgele sıcaklık ve nem değerleri üretiyoruz
        sahte_sicaklik = round(random.uniform(20.0,35.0),2)
        sahte_nem = round(random.uniform(40.0,60.0),2)

        # JSON
        veri_paketi = {
            "cihaz_id": "motor_01",
            "sicaklik": sahte_sicaklik,
            "nem": sahte_nem,
            "zaman_damgasi": int(time.time())
        }

        # Sözlüğü metne çeviriyoruz
        json_mesaj  = json.dumps(veri_paketi)

        # Veriyi Qos=1 seviyesinde gönderiyoruz
        client.publish("factory/room/test",json_mesaj,qos=1)
        print(f" Gönderildi -> {json_mesaj}")
        

        time.sleep(3)
except KeyboardInterrupt:
    print("\nSensör kapatıldı.")
    client.disconnect