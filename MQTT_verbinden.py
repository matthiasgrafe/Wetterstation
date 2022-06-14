#Matthias Grafe
#ETS2021
#µController Projekt
#20.06.2022

#Checkliste zum starten:
#   IoT-Netzwerk verbinden
#   Firewall aus
#   MQTTX starten
#   Node-Red starten

#Verwendete Hardware:
#ESP32
#Breadboard
#HTU2X
#BH1750
#WS2812 LED Stripe

#-------------Bibliotheken aufrufen----------------------------------------------------
import network
import json
from umqtt.simple import MQTTClient
from time import sleep
from neopixel import NeoPixel
from htu2x import HTU21D
from bh1750 import BH1750
from machine import Pin, SoftSPI, SoftI2C       # Pin(BMP180 und TFT), SoftSPI(TFT), SoftI2C(BMP180)
import st7789py as st7789                       # TFT

from fonts import vga2_16x16 as font            # Schriftart laden


i2c = SoftI2C(scl=Pin(22), sda=Pin(21))         # Pins für den i2c Bus
htu = HTU21D(22,21)                             # i2c Bus Anschluss Temperatur und Luftfeuchte
bh = BH1750(i2c)                                # i2c Bus Lichtsensor

#------------Display Initialisierung----------------------------------------------------
spi = SoftSPI(                                  # Objekt spi instanzieren
        baudrate=20000000,                      # TFT Kommunikationsgeschwindigkeit
        polarity=1,                             # 
        phase=0,                                # 
        sck=Pin(18),                            #
        mosi=Pin(19),                           #
        miso=Pin(13))                           #
    
tft = st7789.ST7789(                            # Objekt tft instanzieren
        spi,                                    # Schnittstelle
        135,                                    # Pixel x-Achse(hochkant)
        240,                                    # Pixel y-Achse
        reset=Pin(23, Pin.OUT),                 #
        cs=Pin(5, Pin.OUT),                     #
        dc=Pin(16, Pin.OUT),                    # TEST!!!!!!!!!!!!!!!!!!!!!!!!!!
        backlight=Pin(4, Pin.OUT),              #
        rotation=1)                             # rotation 90°, 2 180°
#-------------Display Initialisierung Ende-----------------

#-------------Neo Pixel Initialisierung---------------
NUM_OF_LED = 5                                  # 5 LED´s von den WS2812 LED´s verwendet
np = NeoPixel(Pin(2), NUM_OF_LED)               # LED Band an Pin 2 angeschlossen

r = 0
g = 0
b = 0

#-------------Clear Stripe-------------------
def clearStripe():
      for i in range(5):
        np[i] = (0,0,0)
        np.write()

#-------------WLAN Manager Schule------------------------------
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

#-------------WLAN zu Hause----------------------------
"""MQTT_Server = "192.168.254..."
CLIENT_ID = "MQTT_MG"
MQTT_TOPIC = "BZTG/Ehnern/E101"
WIFI_SSID = "RepeatRouter"
WIFI_PASSWORT = "*********"
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_SSID,WIFI_PASSWORT)
while not wlan.isconnected():
    pass

print ("wifi connected")
print(wlan.ifconfig())
"""
#---------WLAN Manager Ende----------------------------


#----------MQTT----------------------------------------
mqtt_MG = MQTTClient(CLIENT_ID,MQTT_SERVER)
mqtt_MG.connect()


#----------Werte senden--------------------------------
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



#------------------Werte auf Display---------------------------------
    tft.fill(st7789.BLACK)                                                   
                                                           

    tft.text(font, tempa, 10, 80, st7789.WHITE, st7789.BLACK)
    tft.text(font, "Grad", 150, 80, st7789.WHITE, st7789.BLACK)

    tft.text(font, luft, 10, 100, st7789.WHITE, st7789.BLACK)
    tft.text(font, "%", 150, 100, st7789.WHITE, st7789.BLACK)

    tft.text(font, helligkeit, 10, 100, st7789.WHITE, st7789.BLACK)
    tft.text(font, "LUX", 150, 120, st7789.WHITE, st7789.BLACK)


#----------------LED Anzeige---------------------------------------------
    np[1] = r, g, b
    np[2] = r, g, b
    np[3] = r, g, b

    ledrt = np[1]
    ledgb = np[2]
    ledgn = np[3]


    if luft < 400 and helligkeit < 10:
        r = 0
        g = 80
        b = 0
    
    if (luft >= 400 and luft <= 600) and helligkeit < 10:
        r = 80
        g = 20
        b = 0

    if luft >= 600 and helligkeit < 10:
        r = 80
        g = 0
        b = 0

    if luft < 400 and helligkeit >= 10:
        r = 0
        g = 255
        b = 0
    
    if (luft >= 400 and luft <= 600) and helligkeit >= 10:
        r = 255
        g = 100
        b = 0

    if luft >= 600 and helligkeit >= 10:
        r = 255
        g = 0
        b = 0


