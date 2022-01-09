from config import Config
from flask_session import Session
from flask import Flask

app = Flask(__name__, template_folder='../templates')
app.config.from_object(Config)
Session(app)
