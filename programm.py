"""
from time import sleep                          # Alle 10 Sekunden Temperatur messen
from machine import Pin, SoftSPI, SoftI2C       # Pin(BMP180 und TFT), SoftSPI(TFT), SoftI2C(BMP180)
import st7789py as st7789                       # TFT
from htu2x import HTU21D

from fonts import vga2_16x16 as font            # Schriftart laden
 


i2c = SoftI2C(scl=Pin(22), sda=Pin(21))         # Objekt I2C (BMP180) instanzieren

hum = HTU21D(22, 21)
temp = HTU21D(22, 21)


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


#-------------------------Initialisierung Ende--------------------------

tft.fill(st7789.BLACK)                                                   # Hintergrundfarbe cyan Methode
while True:                                                             # 


        humi = round(hum.humidity)
        humi = str(humi)

        tft.text(font, humi, 10, 80, st7789.WHITE, st7789.BLACK)
        tft.text(font, "Prozent", 150, 80, st7789.WHITE, st7789.BLACK)

        tempa = round(temp.temperature)
        tempa = str(tempa)

        tft.text(font, tempa, 10, 100, st7789.WHITE, st7789.BLACK)
        tft.text(font, "Grad", 150, 100, st7789.WHITE, st7789.BLACK)
"""