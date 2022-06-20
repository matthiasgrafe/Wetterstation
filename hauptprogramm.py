# Matthias Grafe
# ETS2021
# µController Projekt
# 20.06.2022
# Versionsnummer 2.5 vom 20.06.2022



"""
Was macht das Programm?
Ein HTU2X Sensor misst die Temperatur und Luftfeuchtigkeit. Ein BH1750 Helligkeitssensor misst die Helligkeit.  
Die drei Werte werden auf dem TFT Display vom ESP32 ausgegeben.                                                 
Außerdem leuchten die LED´s von einem LED Stripe abhängig von der Luftfeuchtigkeit:                             
rot bei schlechten Werten, gelb bei erhöten Werten und grün bei guten Werten                                    
Die LEDs leuchten in Abhängigkeit von der Helligkeit entweder mit voller Lichtstärke oder gedimmt.              
Die drei Werte werden außerdem als JSON File an MQTTX gesendet und von dort aus weiter verarbeitet.
"""


# Verwendete Hardware:
"""
    ESP32
    HTU2X
    BH1750
    WS2812b
"""

# BUS-Systeme
"""
i2c: 
    BH1750  (Lichtsstärke)
    HTU21   (Temperatur / Luftfeuchtigkeit)
----------
SPI:
    ST7789  (Onboard Display)
----------   
neopixel:
    WS2812b
"""

# Spannungen:
"""
    BH1750 an 3,3V DC
    HTU2X an 3,3V DC
    WS2812b an 5V DC
"""

#####################################################
# Die verwendeten Bibliotheken stehen in der Readme #
#####################################################





#-------------Bibliotheken aufrufen----------------------------------------------------

import json                                     #
from main import MQTT_TOPIC, mqtt_MG            #
from time import sleep, time                    #
from neopixel import NeoPixel                   #
from htu2x import HTU21D                        #
from bh1750 import BH1750                       #
from machine import Pin, SoftSPI, SoftI2C       # Pin(BMP180 und TFT), SoftSPI(TFT), SoftI2C(BMP180)
import st7789py as st7789                       # TFT-Display
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
        dc=Pin(16, Pin.OUT),                    # TEST!
        backlight=Pin(4, Pin.OUT),              #
        rotation=1)                             # rotation 90°, 2 180°
#------------- Display Initialisierung Ende -----------------

#------------- Neo Pixel Initialisierung ---------------
NUM_OF_LED = 11                                 # 11 LED´s von den WS2812 LED´s verwendet
np = NeoPixel(Pin(2), NUM_OF_LED)               # LED Band an Pin 2 angeschlossen

r = 0                                           #
g = 0                                           #
b = 0                                           #

#------------| Funktionen |-------------------
def clearStripe():                              #
      for i in range(NUM_OF_LED):               # Liste für die 11 LED´s           
        np[i] = (0,0,0)                         #
        np.write()                              #

def neoSetzten(r, g, b):                        #
    for i in range(NUM_OF_LED):                 #
        np[i] = (r,g,b)                         #
        np.write()                              #

def convertHelligkeit(x):
    wert = (x - 0) * (254 - 1) // (3000 - 0) + 1
    if wert > 254: wert=254
    return wert
 

mqttSenden = 3                                  # alle 3 sekunden
sensorenAuswerten = 1                           # jede Sekunde
tftAnzeigen = 5                                 # alle 5 Sekunden 

zeitMqtt = time() + mqttSenden
zeitSensoren = time() + sensorenAuswerten
zeitTft = time() + tftAnzeigen                                                      #       

mqtt_MG.connect()                                                                   #

#----------Werte senden--------------------------------
while True:
    if time() >= zeitSensoren:
        try:
            tempa = round(htu.temperature)                                          #
            luft = round(htu.humidity)                                              #
        except:
            print("Temp / Hum sensor kaputt")
            temp = str(0)
            luft = 0
        
        try:
            helligkeit = round(bh.luminance(BH1750.CONT_LOWRES))                    #
        except:
            print("Helligkeit Sensor defekt")                                       #
            helligkeit = 5000                                                       #

        npHell = convertHelligkeit(helligkeit)                                      #

        if luft < 30:                                                               #
            r = 0
            g = 1
            b = 0
        
        if (luft >= 30 and luft <= 50):                                             #
            r = 1
            g = 1
            b = 0

        if luft >= 50:                                                              #
            r = 1
            g = 0
            b = 0

        neoSetzten(r*npHell, g*npHell, b*npHell)                                    #

        ZeitSensoren = time() + sensorenAuswerten                                   #


    if time() >= zeitMqtt:                                                          #
        datatemp = {                                                                #
            "temperatur":{                                                          #
                "HTU21Dtemp": tempa                                                 #
            },
            "luftfeuchte":{                                                         #
                "HTU21Dluft": luft                                                  #
            },
            "helligkeit":{                                                          #
                "BH1750": helligkeit                                                #
            } 
        }
        
        print("MQTT verbunden!")                                                    #
        print(datatemp)                                                             #
        #mqtt_MG.connect() 
        #sleep(0.5)
        mqtt_MG.publish(MQTT_TOPIC,json.dumps(datatemp))                            #
        #sleep(0.5)
        #mqtt_MG.disconnect()

        zeitMqtt = time() + mqttSenden                                              #


#------------------Werte auf Display---------------------------------
    if time() >= zeitTft:                                                           #
        tft.fill(st7789.BLACK)                                                      #        
        tft.text(font, str(tempa) + ' \xf8C', 10, 10, st7789.WHITE, st7789.BLACK)   #

        tft.text(font, str(luft) + ' %', 10, 30, st7789.WHITE, st7789.BLACK)        #

        tft.text(font, str(helligkeit) + ' lux', 10, 50, st7789.WHITE, st7789.BLACK)#

        zeitTft = time() + tftAnzeigen                                              #