from flask import Flask
import os

app = Flask(__name__)

VERSION = os.getenv('VERSION', '1.0')

@app.route('/')
def hello_world():
    return f'Hello, World! Version: {VERSION}'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
