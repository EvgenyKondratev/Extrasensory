from flask import Flask, session
from flask_session import Session

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
    return session.get('key', 'not set')

if __name__ == '__main__':
    app.run()
