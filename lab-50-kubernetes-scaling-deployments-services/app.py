from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello():
    hostname = os.environ.get('HOSTNAME', 'unknown')
    return f'Hello from Pod: {hostname}\n'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
