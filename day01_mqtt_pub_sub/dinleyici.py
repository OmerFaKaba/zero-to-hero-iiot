import paho.mqtt.client as mqtt

# Broker'a başarıyla bağlanılıdğında çalışacak fonksiyon
def on_conncet(client,userdata,flags,reason_code,properties):
    print("Broker'a başarıyla bağlanıldı!")
    # Bağlanır bağlanmaz abone oluyourz
    client.subscribe("factory/room/test")
    print("Kanala abone olundu, veriler bekleniyor...")

# Abone olduğumuz konudan yeni bir veri mesaj geldiğinde çalışıcak fonksiyon
def on_message(client, userdata, msg):
    # Gelen mesajı ekrana yazdırıyoruz (payload byte olarak gelir, decode ile metne çeviriyoruz)
    gelen_mesaj = msg.payload.decode()
    print(f"YENİ VERİ GELDİ -> Konu: {msg.topic} | Mesaj: {gelen_mesaj}")

# MQTT istemicisini (client ) oluşturuyoruz (paho-mqt v2 için API versiyonu belirtilir)
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# Fonksiyonlarımız istemciye tanıtıyoruz
client.on_connect = on_conncet
client.on_message = on_message

# Açık test Broker'ına bağlanıyoruz (1883 standart MQTT portu)
client.connect("broker.emqx.io",1883,60)

# Programın kapanmaması ve sürekli dinlenmesi için sonsuz döngüye sokuyoruz
client.loop_forever()