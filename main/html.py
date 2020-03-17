



import makeJSON
import wifi
import ubinascii
import network
import esp32
import IO
import machine
import network
import ujson
import picoweb
import _thread
import accesspoint

station = network.WLAN(network.STA_IF)
station.active(True)


oldPassword = ''

newPassword = ''

def getSSIDs():
    ssids = []
    file = open("networks.txt", "r")
    for element in file.readlines():
        if element.startswith("ssid: "):
            ssids.append(element[6:].replace('\n', ''))


    return ssids

def getNetworks():
  networks = station.scan()
  names = [x[0].decode('utf-8') for x in networks]
  rssi = [x[3] for x in networks]
  return [names, rssi]

def prepareHtml():
  if wifi.isConnected():
    file = open("wifi.html", "r")
  elif accesspoint.isConnected():
    file = open("accesspoint.html", "r")
  return(file.read())

  
def prepareLogin():
  file = open("logowanie.html", "r")
  return(file.read()) 
  
  
def prepareData():
  toReq = {'id': ubinascii.hexlify(machine.unique_id()),
  'temp': ("%.1f" % ((esp32.raw_temperature() - 32.0) / 1.8)),
  'wifi': IO.States.WIFI(),
  'fuse': IO.States.fuse()}
  
  toReqJSON = ujson.dumps(toReq)
  
  return toReqJSON


def saved(req, resp):
  method = req.method
  if method == "POST":
    yield from req.read_form_data()
    paramsWIFI = req.form
    password = makeJSON.getPassword(paramsWIFI['savednetworks'])
    _thread.start_new_thread(wifi.connectToWIFI, (paramsWIFI['savednetworks'], password))
    accesspoint.stop()
  yield from picoweb.start_response(resp)
  yield from resp.awrite(makeJSON.getSSIDs())

def prepareSSIDs():
  names = getNetworks()[0]
  rssi = getNetworks()[1]
  networkNames = '<thead><tr><th>SSID</th><th>Sygnal</th></tr></thead> \n'
  for (name, signal) in zip(names, rssi):
    networkNames += '<tr><td>' + name + '</td><td>' + str(signal) + '</td><td><input type="radio" value="' + name + '" name="ssid"></td></tr> \n' 
  
  return networkNames

  
def sendNetworks(req, resp):
  yield from picoweb.start_response(resp, content_type = "application/json")
  yield from resp.awrite(prepareSSIDs())

  

def change(req, resp):
  global oldPassword
  global newPassword
  method = req.method
  if method == "POST":
    yield from req.read_form_data()
    paramsLogging = req.form
    newPassword = paramsLogging["password"]
    oldPassword = paramsLogging["oldpassword"]
    if makeJSON.isOldPassword(oldPassword) and len(newPassword) >= 8:
      makeJSON.saveAPPassword(newPassword)
    
  yield from picoweb.start_response(resp)
  yield from resp.awrite(prepareLogin())


 
def changepass(req, resp):
  global oldPassword
  global newPassword
  print(newPassword, oldPassword)
  oldPassword = newPassword
  yield from picoweb.start_response(resp)
  if oldPassword != '' and newPassword != '':
    yield from resp.awrite(makeJSON.isPasswordsOk(newPassword, oldPassword))
  else:
    yield from resp.awrite('0')
  
  
 
def index(req, resp):
  method = req.method
  if method == "POST":
    yield from req.read_form_data()
    paramsWIFI = req.form
    ssid = paramsWIFI["ssid"]
    password = paramsWIFI["password"]
    _thread.start_new_thread(wifi.connectToWIFI, (ssid, password))
    accesspoint.stop()
  elif method == "GET":
    yield from picoweb.start_response(resp)
    yield from resp.awrite(prepareHtml())
  

def data(req, resp):
  yield from picoweb.start_response(resp, content_type = "application/json")
  yield from resp.awrite(prepareData())

  
  
ROUTES = [("/", index),("/data", data),("/networks", sendNetworks),("/saved", saved),("/changepassword", change),("/change",changepass )]

HTTPServer = picoweb.WebApp(__name__, ROUTES)

def start():
  HTTPServer.run(debug=True, host = "192.168.1.254")








