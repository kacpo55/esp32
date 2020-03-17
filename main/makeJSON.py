


import ujson


state = False

def saveNetwork(ssid, password):
  file = open("networks.txt", "r")
  jsonfile = ujson.load(file)
  file.close()
  file = open("networks.txt", "w")
  jsonfile[ssid] = password
  file.write(ujson.dumps(jsonfile))
  file.close()

def getSSIDs():
  ssids = '<thead><tr><th>Zapisane sieci</th></tr></thead> \n'
  file = open("networks.txt", "r")
  jsonfile = ujson.load(file)
  for key in jsonfile:
    ssids += '<tr><td>' + str(key) + '</td><td><input type="radio" value="' + str(key) + '" name="savednetworks"></td></tr> \n'
  return ssids
  
def getPassword(key):
  file = open("networks.txt", "r")
  jsonfile = ujson.load(file)
  return jsonfile[key]

  
def isOldPassword(password):
  file = open("logindata.txt", "r")
  jsonfile = ujson.load(file)
  file.close()
  oldPassword = jsonfile["password"]
  if oldPassword == password:
    return True
  else:
    return False
  
def saveAPPassword(password):
  file = open("logindata.txt", "r")
  jsonfile = ujson.load(file)
  file.close()
  file = open("logindata.txt", "w")
  jsonfile["password"] = password
  file.write(ujson.dumps(jsonfile))
  file.close()

def isPasswordsOk(password, oldPassword):
  if len(password) < 8:
    return "Nowe haslo jest za krotkie"
  
  if not isOldPassword(oldPassword):
    return "Stare haslo sie nie zgadza"
  
  else:
    return "0"
  
def getAPPassword():
  file = open("logindata.txt", "r")
  jsonfile = ujson.load(file)
  password = jsonfile["password"]
  return str(password)





