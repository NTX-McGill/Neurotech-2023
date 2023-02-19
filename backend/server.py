from flask import Flask, render_template, request
from flask_socketio import SocketIO
from random import random
from threading import Lock
from datetime import datetime
from datastream import startStream


thread = None
thread_lock = Lock()

"""Intialising Flask and socket"""
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app, cors_allowed_origins="*")


app.host = 'localhost'

def get_current_datetime():
    now = datetime.now()
    return now.strftime("%m/%d/%Y %H:%M:%S")



def background_thread():
    while True:
        data = startStream() # Calling startstream() from datastream.py to start collecting the signals
        print("sending")
        socketio.emit('data', {'value': data, "date": get_current_datetime()})
        socketio.sleep(1)
        
        


"""
Decorator for connect
"""
@socketio.on('connect')
def connect():
    global thread
    print('Client connected')

    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)

"""
Decorator for disconnect
"""
@socketio.on('disconnect')
def disconnect():
    print('Client disconnected',  request.sid)

if __name__ == '__main__':
    socketio.run(app, debug=True)

