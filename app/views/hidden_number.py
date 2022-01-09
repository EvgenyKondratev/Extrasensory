from main_app import app
from flask import render_template, request, redirect, url_for
from flask.views import MethodView
from forms.hidden_number import HiddenNumberForm
from models.hidden_numbers import HiddenNumbers
from models.extrasensory import Extrasensory


class HiddenNumberView(MethodView):
    def get(self):
        form = HiddenNumberForm()

        hidden_numbers = HiddenNumbers.load() or HiddenNumbers([])

        extrasensories = []
        extrasensory_count = app.config.get('EXTRASENSORY_COUNT', 0)
        for i in range(extrasensory_count):
            extrasensory = Extrasensory.load(str(i)) or Extrasensory(str(i), 0, [])
            if len(hidden_numbers.numbers) == len(extrasensory.predictions):
                extrasensory.predict()
                extrasensory.save()
            extrasensories.append(extrasensory)

        return render_template('hidden-number.html', form=form, extrasensories=extrasensories)

    def post(self):
        form = HiddenNumberForm()
        if form.validate_on_submit():
            extrasensory_count = app.config.get('EXTRASENSORY_COUNT', 0)
            extrasensories = [Extrasensory.load(str(i)) for i in range(extrasensory_count)]
            extrasensories = [ext for ext in extrasensories if ext is not None]

            hidden_number = int(request.form['hidden_number'])
            hidden_numbers = HiddenNumbers.load() or HiddenNumbers([])
            hidden_numbers.numbers.append(hidden_number)

            if len(extrasensories) > 0 and len(extrasensories[0].predictions) == len(hidden_numbers.numbers):
                hidden_numbers.save()
                for ext in extrasensories:
                    ext.recalc_accuracy(hidden_number)
                    ext.save()

            return redirect(url_for('index'))
        else:
            return redirect(url_for('hidden_number'))
