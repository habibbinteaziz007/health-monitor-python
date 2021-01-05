from flask import Flask
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import random
import requests

app = Flask(__name__)


@app.route('/')
def index():
    return "Hey There"


@app.route('/submit/temperature/<temperature>')
def submit_temperature(temperature):
    fahrenheit = (int(temperature) * 1.8) + 32
    link = 'http://developer.muthofun.com/sms.php?username=hasanmahmud&password=hAsAn.420&mobiles=01625376336&sms=Critical Temperature&uniccode=1'
    if fahrenheit >= 100:
        requests.get(url=link)
        print("SMS SEND")

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
