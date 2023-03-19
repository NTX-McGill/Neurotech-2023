from flask import Flask, render_template, request
from flask_socketio import SocketIO
from random import random
from threading import Lock
from datetime import datetime
import time
from datastream import startStream
from plotData.brainflowGetData import start


thread = None
thread_lock = Lock()

"""Intialising Flask and socket"""
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app, cors_allowed_origins="*")


app.host = 'localhost'

def get_current_datetime():
    now = datetime.now()
    # Return UNIX timestamp
    return time.mktime(now.timetuple())
    # return now.strftime("%m/%d/%Y %H:%M:%S")



def background_thread():
    while True:
        data = start() 
        print("sending")
        socketio.emit("Started collection...")
        socketio.sleep(1)
        
        
        
@app.route("/connect", methods=["POST"], strict_slashes=False)
def connect():
    start()


# """
# Decorator for connect
# """
# @socketio.on('connect')
# def connect():
#     global thread
#     print('Client connected')

#     global thread
#     with thread_lock:
#         if thread is None:
#             thread = socketio.start_background_task(background_thread)

# """
# Decorator for disconnect
# """
# @socketio.on('disconnect')
# def disconnect():
#     print('Client disconnected',  request.sid)

if __name__ == '__main__':
    socketio.run(app, debug=True)

