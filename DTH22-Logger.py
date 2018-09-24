#!usr/bin/python3
# DTH22-Logger.py

'''
Vorbereitung:
AM2302:
sudo apt-get update
sudo apt-get install build-essential python-dev python-openssl git
git clone https://github.com/adafruit/Adafruit_Python_DHT.git
cd Adafruit_Python_DHT
sudo python3 setup.py install

or install with pip
sudo pip3 install Adafruit_DHT

Information from -> https://tutorials-raspberrypi.de/raspberry-pi-luftfeuchtigkeit ->
-temperatur-messen-dht11-dht22/


Autor   : Christian Dopatka
Version : 29.05.2017
Version : 24.09.2018    - Druckluftsensor (BMP085) entfernt
                        - Speichern in eine Datenbank hinzugefügt [UNGETESTET]




License:  Creative Commons CC BY-NC
https://creativecommons.org/licenses/?lang=de
'''

import csv
import time
import Adafruit_DHT
import sqlite3

## Der Sensor:
_am2302 = Adafruit_DHT.AM2302
pin = 17

# Für die Plausibilitätsprüfung
_oldTemperature
_oldHumidity

def measure():
    (humidity, temperature) = Adafruit_DHT.read_retry(_am2302, pin)
    return(temperature, humidity)

def averageMinute():
    temperatureList                         = []
    humidityList                            = []
    pressureList                            = []
    minOld                                  = time.strftime("%M")
    minNew                                  = time.strftime("%M")
    while minOld == minNew:
        (temperature, humidity)   = measure()
        if temperature is not None and plausibilityTest(_oldTemperature, temperature) == True:
            temperatureList.extend([temperature])
            global _oldTemperature = temperature
        if humidity is not None and plausibilityTest(_oldHumidity, humidity) == True:
            humidityList.extend([humidity])
            global _oldHumidity = humidity
        time.sleep(5)
        minNew                      = time.strftime("%M")
    temperature                     = sum(temperatureList)/len(temperatureList)
    humidity                        = sum(humidityList)/len(humidityList)

    return (temperature, humidity)

def plausibilityTest(valueOld, valueNew):
    compareValueMin = valueOld - valueOld * 0.2
    compareValueMax = valueOld + valueOld * 0.2
    if valueNew < compareValueMax and valueNew > compareValueMin:
        plausibility = True
    else:
        plausibility = False

    return(plausibility)

def connectToDataBase():

    # UNGETESTET

    conn = sqlite3.connect("temp.db")
    cursor = conn.cursor()

    # Create table
    sql = '''CREATE TABLE IF NOT EXISTS temperature
                 (temp REAL, humm REAL datetime TIME)'''
    cursor.execute(sql)

    # Save (commit) the changes
    conn.commit()

    return (conn)

def writeDataIntoDataBase(conn ,temperature, humidity):

    # UNGETESTET

    cursor = conn.cursor()
    dateTime = time.strftime("YYYY-MM-DD HH:MM:SS.SSS")

    format_str = """INSERT INTO temperature (temp, hum, datetime) 
    VALUES ("{t}", "{h}", "{dt}");"""

    sql = format_str.format(t=temperature, h=humidity, dt=dateTime)
    cursor.execute(sql)

    # Save (commit) the changes
    conn.commit()




# Now start the Programm....

# check for Errors
try:

    # Connected to the Database
    conn = connectToDataBase()

    # Always true
    while True:
        (temperature, humidity)             = averageMinute()
        Hour                                = time.strftime("%H")
        Minute                              = time.strftime("%M")
        Date                                = time.strftime("%d_%m_%Y")
        Day                                 = time.strftime("%d")
        Mounth                              = time.strftime("%m")
        Year                                = time.strftime("%Y")

        # Save into the Database
        writeDataIntoDataBase(conn, temperature, humidity)

        # Save into CSV-Files
        FileTemperature = '/home/cris/Dokumente/Wetterstation/ \
        Messdaten/temperature/' + Date + '.csv'
        FileHumidity = '/home/cris/Dokumente/Wetterstation/ \
        Messdaten/humidity/' + Date + '.csv'
        # In die CSV-Dateien schreiben
        with open(FileTemperature,'a') as out:
            file    = csv.writer(out, delimiter=';', lineterminator='\n')
            file.writerow([temperature,Houre,Minute,Day,Mounth,Year])
        out.close()
        with open(FileHumidity,'a') as out:
            file    = csv.writer(out, delimiter=';', lineterminator='\n')
            file.writerow([humidity,Houre,Minute,Day,Mounth,Year])
        out.close()

# Do by Error or by clothing Script
finally:
    conn.close()