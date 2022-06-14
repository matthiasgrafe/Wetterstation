#Matthias Grafe
#ETS2021
#µController Projekt

#Checkliste 
#IoT-Netzwerk verbinden
#Firewall aus
#MQTTX starten
#Node-Red starten

#-------------Bibliotheken aufrufen----------------------------------------------------
import network
import json
from umqtt.simple import MQTTClient
from time import sleep
from htu2x import HTU21D
from bh1750 import BH1750
from machine import Pin, SoftSPI, SoftI2C       # Pin(BMP180 und TFT), SoftSPI(TFT), SoftI2C(BMP180)
import st7789py as st7789                       # TFT

from fonts import vga2_16x16 as font            # Schriftart laden
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
htu = HTU21D(22,21)
bh = BH1750(i2c)
#------------Display Initialisierung----------------------------------------------------
spi = SoftSPI(                                  # Objekt spi instanzieren
        baudrate=20000000,                      # TFT Kommunikationsgeschwindigkeit
        polarity=1,                             # 
        phase=0,                                # 
        sck=Pin(18),                            #
        mosi=Pin(19),                           #
        miso=Pin(13))                           #
    
tft = st7789.ST7789(                                                    # Objekt tft instanzieren
        spi,                                                            # Schnittstelle
        135,                                                            # Pixel x-Achse(hochkant)
        240,                                                            # Pixel y-Achse
        reset=Pin(23, Pin.OUT),                                         #
        cs=Pin(5, Pin.OUT),                                             #
        dc=Pin(16, Pin.OUT),                                            # TEST!!!!!!!!!!!!!!!!!!!!!!!!!!
        backlight=Pin(4, Pin.OUT),                                      #
        rotation=1)                                                     # rotation 90°, 2 180°
#-------------Display Initialisierung Ende-----------------

#-------------WLAN Manager------------------------------
MQTT_SERVER = "192.168.1.231"
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
#---------WLAN Manager Ende----------------------------

#----------MQTT
mqtt_MG = MQTTClient(CLIENT_ID,MQTT_SERVER)
mqtt_MG.connect()

while True:
    tempa = round(htu.temperature)
    luft = round(htu.humidity)
    helligkeit = round(bh.CONT_LOWRES)

    datatemp = {
        "temperatur":{
            "HTU21D": str(tempa)
        },
        "luftfeuchte":{
            "HTU21D": str(luft)
        },
        "helligkeit":{
            "BH1750": str(helligkeit)
        } 
    }
    
    print("MQTT verbunden!")
    print(datatemp)
    mqtt_MG.publish(MQTT_TOPIC,json.dumps(datatemp))
    sleep(2)
    #mqtt_MG.disconnect()


