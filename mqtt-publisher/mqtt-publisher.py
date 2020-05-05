#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
	Simple UDP broadcast listener for temperature sensor network
"""

# imports
import sys, os, syslog
import calendar, datetime, time
import socket
import json
import sqlite3
import paho.mqtt.client as mqtt
import shutil
import inspect

# init

LLAP_PORT = 50140

MQTT_BROKER = "mqtt.lan"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 600
TOPIC_BASE = "places/home/"
LWT_TOPIC = "clients/llap-bridge"
LWT_ALIVE = "1"
LWT_DEAD = "0"

if os.path.exists(path): 
  print("Configuration file exists")
else:
  print("No configuration file, copying default settings")
  


sensorlocation = {
	'AA' : 'winecellar',
	'AB' : 'kitchen',
	'AC' : 'guestroom',
	'AD' : 'office',
	'AE' : 'livingroom',
	'BA' : 'cigarhumidor'
}

# some functions

def on_connect(mosq, obj, rc):
    print("Connected to MQTT Broker")

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("%s: Unexpected disconnection" % (time.strftime("%b %d %H:%M:%S")))
    print("%s: Reconnecting" & (time.strftime("%b %d %H:%M:%S")))
    mqttc.reconnect()

def on_publish(client, userdata, mid):
    print("%s: MQTT message published: %s" % (time.strftime("%b %d %H:%M:%S", time.localtime())))


# get ready to receive UDP transmissions

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
sock.bind(('', LLAP_PORT))

# get ready to publish MQTT messages

mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_disconnect = on_disconnect
mqttc.on_publish = on_publish
mqttc.will_set(LWT_TOPIC, payload=LWT_DEAD, qos=0, retain=True)
mqttc.reconnect_delay_set(min_delay=30, max_delay=3000)
mqttc.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)

# ready to go

print("%s: Python version %s" % (time.strftime("%b %d %H:%M:%S", time.localtime()), sys.version ))
print("%s: LLAP to MQTT bridge up (PID %s)" % (time.strftime("%b %d %H:%M:%S", time.localtime()), str(os.getpid())))
print("%s: Listening on UDP port %s" % (time.strftime("%b %d %H:%M:%S", time.localtime()), str(LLAP_PORT)))
print("%s: Publishing on MQTT broker at %s, port %s" % (time.strftime("%b %d %H:%M:%S", time.localtime()), str(MQTT_BROKER), str(MQTT_PORT)))

syslog.syslog("LLAP to MQTT bridge up")
mqttc.publish(LWT_TOPIC, LWT_ALIVE, qos=0, retain=True)

# start listening

while True:

    data, addr = sock.recvfrom(1024)
    pydata = json.loads(data)

    print("%s: Received incoming transmission: %s" % (time.strftime("%b %d %H:%M:%S", time.localtime()), str(pydata)))
    syslog.syslog("Received incoming message: " + str(pydata))

    if pydata['type'] == 'WirelessMessage':

        sensor_address = pydata['id']
        sensor_location = sensorlocation[sensor_address]

        print("%s: LLAP message in incoming transmission. Sensor %s transmitted %s" % ( time.strftime("%b %d %H:%M:%S", time.localtime()), str(sensor_address), str(pydata['data'][0]) ))

        if pydata['data'][0][:4] == "TEMP":

            temperature = '%s' % pydata['data'][0][-4:]

            print("%s: Publishing temperature reading for %s sensor: %s" % (time.strftime("%b %d %H:%M:%S", time.localtime()), str(sensor_location) ,str(temperature)))
            mqttc.publish(TOPIC_BASE + str(sensor_location) + "/temperature", str(temperature))

        if pydata['data'][0][:4] == "RHUM":

            relative_humidity = '%s' % pydata['data'][0][-4:]

            print("%s: Publishing relative humidity reading for %s sensor: %s" % (time.strftime("%b %d %H:%M:%S", time.localtime()), str(sensor_location) ,str(relative_humidity)))
            mqttc.publish(TOPIC_BASE + str(sensor_location) + "/relative-humidity", str(relative_humidity))

        if pydata['data'][0][:4] == "BATT":

           battery = '%s' % pydata['data'][0][-4:]
           print("%s: Publishing battery voltage reading for %s sensor: %s" % (time.strftime("%b %d %H:%M:%S", time.localtime()), str(sensor_location) ,str(battery)))
           mqttc.publish(TOPIC_BASE + str(sensor_location) + "/battery", str(battery))

    else:

           print("%s: Transmission does not contain an LLAP message, discarding" % (time.strftime("%b %d %H:%M:%S", time.localtime())))

mqttc.disconnect()
