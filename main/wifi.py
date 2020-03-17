

import accesspoint
import utime
import network
import IO
import html
import _thread
import makeJSON
import states

def isConnected():
  station = network.WLAN(network.STA_IF)
  return station.isconnected()


def stop():
  station = network.WLAN(network.STA_IF)
  station.active(False)


def connectToWIFI(ssid, password):
  timeout = 20
  seconds = 0
  states.isConnecting(True)
  station = network.WLAN(network.STA_IF)
  station.active(True)
  station.ifconfig(('192.168.1.254', '255.255.0.0', '192.168.0.1', '8.8.8.8'))
  if not station.isconnected():
      station.connect(ssid, password)
      while not station.isconnected():
          utime.sleep(1)
          seconds += 1
          if seconds >= timeout:
            states.isConnecting(False)
            station.disconnect()
            accesspoint.start()
            break
  
  states.isConnecting(False)
  if station.isconnected():
    makeJSON.saveNetwork(ssid, password)
    _thread.start_new_thread(html.start, ())








