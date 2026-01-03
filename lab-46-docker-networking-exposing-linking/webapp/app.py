from flask import Flask
import os
import socket

app = Flask(__name__)

@app.route('/')
def hello():
    hostname = socket.gethostname()
    return f'Hello from {hostname}!\n'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')