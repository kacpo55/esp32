

import makeJSON
import network
import _thread
import html


def isConnected():
  accesspoint = network.WLAN(network.AP_IF)
  return accesspoint.isconnected()

def stop():
  accesspoint = network.WLAN(network.AP_IF)
  accesspoint.active(False)

def start():
  accesspoint = network.WLAN(network.AP_IF)
  accesspoint.active(True)   

def makeAccesspoint():
  accesspoint = network.WLAN(network.AP_IF)
  accesspoint.active(True)
  accesspoint.ifconfig(('192.168.1.254', '255.255.0.0', '192.168.0.1', '8.8.8.8'))
  if len(makeJSON.getAPPassword()) >= 8:
    accesspoint.config(essid='ESP32-CONFIG', password=makeJSON.getAPPassword(), authmode=4)
  else:
    accesspoint.config(essid='ESP32-CONFIG')
  _thread.start_new_thread(html.start, ())






