import network
import json
from umqtt.simple import MQTTClient
from time import sleep
from htu2x import HTU21D



MQTT_SERVER = "10.50.217.103"
CLIENT_ID = "MQTT_MG"
MQTT_TOPIC = "BZTG/Ehnern/E101"
WIFI_SSID = "BZTG-IoT"
WIFI_PASSWORT = "WerderBremen24"



wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_SSID,WIFI_PASSWORT)
while not wlan.isconnected():
    pass

print ("wifi connected")
print(wlan.ifconfig())



while True:
    tempa = HTU21D.temperature
    datatemp = {
        "Temperatur":
        {
            str(tempa)
        }
    }
    mqtt_MG = MQTTClient(CLIENT_ID,MQTT_SERVER)
    mqtt_MG.connect()

    print("MQTT verbunden!")
    mqtt_MG.publish(MQTT_TOPIC,json.dumps(datatemp))
    sleep(1)
    mqtt_MG.disconnect()


