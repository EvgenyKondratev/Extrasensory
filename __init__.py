from flask import Flask, session
from flask_session import Session
import redis

app = Flask(__name__)

SESSION_TYPE = 'redis'
app.config.from_object(__name__)
Session(app)

@app.route('/')
def hello_Flask():
    return 'Hello Flask!!!'

@app.route('/set/')
def set():
    session['key'] = 'value'
    return 'ok'

@app.route('/get/')
def get():
    r = redis.Redis(host='localhost', port=6379, db=0)
    s = ''
    for key in r.scan_iter():
        s += f'{key}: {r.get(key)}<br/>'
        print(key, r.get(key))
    return s if s != '' else 'not set' #session.get('key', 'not set')

if __name__ == '__main__':
    app.run()
