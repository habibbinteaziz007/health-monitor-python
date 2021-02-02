from flask import Flask
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import random
import requests
from twilio.rest import Client

app = Flask(__name__)


@app.route('/')
def index():
    return "Hey There"


@app.route('/submit/temperature/<temperature>')
def submit_temperature(temperature):
    fahrenheit = (int(temperature) * 1.8) + 32
    if fahrenheit >= 100:
        account_sid = 'AC8b072243584c48f9362b4783cbadd8f0' 
        auth_token = '34acedcefc97342e772c813feb7daac8' 
        client = Client(account_sid, auth_token)
        message = client.messages.create(  messaging_service_sid='MGa12bc9fb5d436e3903e7eeaf8e09eb5f',to='+8801625376336',body='Patient body temperature is '+str(int(fahrenheit))+' F') 
        print(message.sid)

    if len(firebase_admin._apps) == 0:
        cred = credentials.Certificate('./service.json')
        firebase_admin.initialize_app(cred, {'databaseURL': 'https://health-monitor-c2352-default-rtdb.firebaseio.com/',
                                                 'databaseAuthVariableOverride': None})
    db.reference("temperature").push().set({'value': int(temperature)})
    return "done"


@app.route('/submit/heartbeat/<heartbeat>')
def submit_heartbeat(heartbeat):
    heartbeat = random.randrange(81, 97)
    if len(firebase_admin._apps) == 0:
        cred = credentials.Certificate('./service.json')
        firebase_admin.initialize_app(cred, {'databaseURL': 'https://health-monitor-c2352-default-rtdb.firebaseio.com/',
                                             'databaseAuthVariableOverride': None, })
    db.reference("heartbeat").push().set({'value': int(heartbeat)})
    return "done"


if __name__ == "__main__":
    app.run(debug=True)
