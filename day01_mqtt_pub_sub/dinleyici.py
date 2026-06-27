import paho.mqtt.client as mqtt
import json
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# --- INFLUXDB BAĞLANTI AYARLARI ---
# Docker'ı ayağa kaldırırken verdiğimiz parametrelerin birebir aynısı olmak zorunda
INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "supergizlitoken123"
INFLUX_ORG = "wisersense"
INFLUX_BUCKET = "sensor_verileri"

# InfluxDB istemcisini ve yazma API'sini başlatıyoruz
influx_client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = influx_client.write_api(write_options=SYNCHRONOUS)

# --- MQTT AYARLARI ---
def on_connect(client, userdata, flags, reason_code, properties):
    print("Broker'a başarıyla bağlanıldı!")
    # Kanala QoS=1 ile abone oluyoruz
    client.subscribe("factory/room/test", qos=1)
    print("Kanala abone olundu, veriler InfluxDB'ye yazılmak üzere bekleniyor...")

def on_message(client, userdata, msg):
    try:
        # 1. Gelen byte verisini string'e çevir ve JSON olarak yükle
        mesaj_str = msg.payload.decode()
        veri = json.loads(mesaj_str)
        print(f"MQTT'den Yeni Veri Alındı: {veri}")
        
        # 2. InfluxDB için bir veri noktası (Point) oluşturuyoruz
        # 'measurement' SQL'deki tablo adı gibidir. Biz 'motor_sensorleri' dedik.
        nokta = Point("motor_sensorleri") \
            .tag("cihaz_id", veri["cihaz_id"]) \
            .field("sicaklik", veri["sicaklik"]) \
            .field("nem", veri["nem"])
            # Not: Zaman damgası eklemezsek InfluxDB o anki sistem saatini otomatik ekler.
            
        # 3. Oluşturulan noktayı veritabanına yazıyoruz
        write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=nokta)
        print("Veri başarıyla InfluxDB'ye kaydedildi.\n")
        
    except Exception as e:
        print(f"Veri işlenirken hata oluştu: {e}")

# MQTT İstemci Kurulumu
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect("broker.emqx.io", 1883, 60)
mqtt_client.loop_forever()