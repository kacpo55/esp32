
from IO import *
import network

station = network.WLAN(network.STA_IF)
  
  
def isConnecting(state):
  global connectingWIFI
  connectingWIFI = state


def checkState():
  global connectingWIFI
  connectingWIFI = False
  
  while True:
    
    while connectingWIFI:
      Led.connectingToWIFI()
    
    if IO.getStates() == [1,0]:
      
      if station.isconnected():
        Led.fuseOkWIFIOk()
      
      elif not station.isconnected():
        Led.fuseOkWIFINaN()
      
    else:
        
      if station.isconnected():
        Led.fuseNaNWIFIOk()
        
      else:
        Led.fuseNaNWIFINaN()


