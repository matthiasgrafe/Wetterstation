import network
from umqtt.simple import MQTTClient

#-------------WLAN Manager Schule------------------------------
MQTT_SERVER = "192.168.1.206"                   #               
CLIENT_ID = "MQTT_MG"                           #
MQTT_TOPIC = "BZTG/Ehnern/E101"                 #
WIFI_SSID = "BZTG-IoT"                          #
WIFI_PASSWORT = "WerderBremen24"                #



wlan = network.WLAN(network.STA_IF)
wlan.active(True)

if not wlan.isconnected():
    wlan.connect(WIFI_SSID, WIFI_PASSWORT)
    while wlan.isconnected() == False:
        pass
    
    print()
    print('Connection successful')
    print(wlan.ifconfig())
    print()

print ("wifi connected")                        #
print(wlan.ifconfig())                          #
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
mqtt_MG = MQTTClient(CLIENT_ID,MQTT_SERVER)     #
                              #