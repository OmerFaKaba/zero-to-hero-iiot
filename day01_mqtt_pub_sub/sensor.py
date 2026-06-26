import paho.mqtt.client as mqtt
import time
import random

# MQTT istemcisini oluşturuyoruz 
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# Aynı test Broker'ına bağlanıyoruz
client.connect("broker.emqx.io",1883,60)

print("Sensör çalışmaya başladı. Veri gönderiliyor...")

# Sensör sürekli çalışsın diye bir döngü kuruyoruz
try:
    while True:
        # Rastgele bir sıcaklık değeri üretiyoruz (örneğin 20.0 ile 30.0 arası)
        sahte_sicaklik = round(random.uniform(20.0,30.0),2)
        mesaj = f"Motor Sicakligi: {sahte_sicaklik} C"

        # Ürettiğimiz veriyi 'factory/room/test' topic'e gönderiyoruz
        client.publish("factory/room/test",mesaj)
        print(f"Gönderildi: {mesaj}")

        # Sensör 3 saniyede bir veri göndersin
        time.sleep(3)

except KeyboardInterrupt:
    print("\nSensör kapatıldı")
    client.disconnect()