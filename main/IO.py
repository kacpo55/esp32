
import wifi
import network
from machine import Pin
import utime
ledR = Pin(13,Pin.OUT)
ledG = Pin(27,Pin.OUT)
ledB = Pin(12,Pin.OUT)
IN1 = Pin(22,Pin.IN)
IN2 = Pin(23,Pin.IN)


station = network.WLAN(network.STA_IF)

class Led():
  
  def connectingToWIFI():
    Led.write(0,0,1)
    
  def fuseOkWIFINaN():
    Led.write(0,1,0)
    
  def fuseOkWIFIOk():
    Led.write(0,1,0)
    utime.sleep(1)
    Led.write(0,0,1)
    utime.sleep(1)
    
  def fuseNaNWIFIOk():
    Led.write(0,0,1)
    utime.sleep(1)
    Led.write(1,0,0)
    utime.sleep(3)
    
  def fuseNaNWIFINaN():
    Led.write(1,0,0)
    
  def write(red, green, blue):
    ledR.value(red)
    ledG.value(green)
    ledB.value(blue)
    
  def clear():
    Led.write(0,0,0)

class IO():
  
  def getStates():
    return [IN1.value(), IN2.value()]

class States():
  
  def fuse():
    if IO.getStates() == [1,0]:
      return "OK"
    if IO.getStates() == [0,1]:
      return "ZUZYTY"
    if IO.getStates() == [1,1]:
      return "BRAK"
    if IO.getStates() == [0,0]:
      return "ZWARCIE"
      
  def WIFI():
    if station.isconnected():
      return station.config('essid')
    if not station.isconnected():
      return "BLAD"


