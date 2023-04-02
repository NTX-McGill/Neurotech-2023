from flask import Flask, render_template, request
from flask_socketio import SocketIO
from flask_cors import CORS, cross_origin
from random import random
from threading import Lock
from datetime import datetime
import time

from plotData.brainflowGetData import start


thread = None
thread_lock = Lock()

"""Intialising Flask and socket"""
app = Flask(__name__)
cors = CORS(app)
app.config['SECRET_KEY'] = 'secret'
app.config['CORS_HEADERS'] = 'Content-Type'
socketio = SocketIO(app, cors_allowed_origins="*")


app.host = 'localhost'






        
@app.route("/connect", methods=["POST"], strict_slashes=False)
def connect():
    data = request.get_json()
    print(data)
    
    return data
    

if __name__ == '__main__':
    print("cdfff")
    app.run()

