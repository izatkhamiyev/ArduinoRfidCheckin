from firebase import firebase
from time import gmtime, strftime
import pyrebase
import json
import time
from serial import Serial

# config = {
#   "apiKey": "c43247527306b47f0071738d0eff9d2842edf96a",
#   "authDomain": "projectId.firebaseapp.com",
#   "databaseURL": "https://databaseName.firebaseio.com",
#   "storageBucket": "projectId.appspot.com"
# }

# firebase = pyrebase.initialize_app(config)
# db = firebase.database()
firebase = firebase.FirebaseApplication("https://smart-sockets.firebaseio.com/")

def fetch_data():
    arduino = Serial("COM6", 9600)
    arduino.flushInput()
    arduino.flushOutput()
    data = arduino.readline()
    arduino.flushInput()
    arduino.flushOutput()
    data = arduino.readline()
    arduino.flushInput()
    arduino.flushOutput()
    data = arduino.readline()
    return data


def filter_data(line):
    tmp = str(line[-13:-2])[2:-1]
    return ''.join(tmp.split())


def update_db(data):
    result = firebase.get('/users', None)
    openDoor = False
    for key, value in result.items():
        if value['id'] == data:
            firebase.put('/users/' + key, "in", value["in"]^1)
            openDoor = True
    return openDoor

while(True):
    line = fetch_data()
    x = filter_data(line)
    update_db(x)
    print(x)
