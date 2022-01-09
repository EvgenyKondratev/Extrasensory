from main_app import app
from flask import render_template, redirect, url_for
from flask.views import MethodView
from models.hidden_numbers import HiddenNumbers
from models.extrasensory import Extrasensory


class IndexView(MethodView):
    def get(self):
        hidden_numbers = HiddenNumbers.load()
        extrasensory_count = app.config.get('EXTRASENSORY_COUNT', 0)
        extrasensories = [Extrasensory.load(str(i)) for i in range(extrasensory_count)]
        extrasensories = [ext for ext in extrasensories if ext is not None]
        return render_template('index.html',
                               hidden_numbers=hidden_numbers,
                               extrasensories=extrasensories)

    def post(self):
        return redirect(url_for('hidden_number'))
