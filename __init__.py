from flask import Flask, session, request, redirect, url_for, render_template
from flask_session import Session
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import ValidationError, DataRequired, NumberRange

import random

app = Flask(__name__)

SESSION_TYPE = 'redis'
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'R2dS*4Wqe#Q2%7mgW{seP7R?'
Session(app)

extrasensory_count = 30  # Количество экстросенсов
beg = 10  # Минимальное двухзначное число
end = 99  # Максимальное двухзначное число


class MyValueForm(FlaskForm):
    myvalue = IntegerField(label='Введите загаданное двухзначное число',
                           validators=[DataRequired(), NumberRange(min=beg, max=end)])
    submit = SubmitField(label='Отправить')


def get_extrasensory_data():
    ext_accuracy = {}
    ext_vals = {}
    for i in range(extrasensory_count):
        ext_accuracy[i] = session.get(f'ext_accuracy:{i}', 0)
        ext_vals[i] = session.get(f'ext_vals:{i}', [])
    return (ext_accuracy, ext_vals)


def extrasensory_predict():
    for i in range(extrasensory_count):
        random_integer = random.randint(beg, end)
        session.get(f'ext_vals:{i}', []).append(random_integer)

        if not session.modified:
            session.modified = True

    session['num'] = session.get('num', 0) + 1


def get_extrasensory_value(example_count=3):
    ret = {}
    j = 0
    while j < example_count:
        idx = random.randint(0, extrasensory_count - 1)
        if idx not in ret:
            vals = session.get(f'ext_vals:{idx}', [])
            ret[idx] = vals[-1] if len(vals) > 0 else -1
            j += 1

    return ret


def calc_extrasensory_level(value):
    for i in range(extrasensory_count):
        vals = session.get(f'ext_vals:{i}', [])
        if value == (vals[-1] if len(vals) > 0 else -1):
            session[f'ext_accuracy:{i}'] = session.get(f'ext_accuracy:{i}', 0) + 1
        else:
            acc = session.get(f'ext_accuracy:{i}', 0)
            if acc > 0:
                session[f'ext_accuracy:{i}'] = acc - 1


@app.route('/input_val', methods=['GET', 'POST'])
def input_val():
    form = MyValueForm()
    if form.validate_on_submit():
        vals_count = len(session.get('myvals', []))
        num = session.get('num', 0)

        if(vals_count < num):
            myvalue = request.form['myvalue']
            session.get('myvals', []).append(int(myvalue))
            if not session.modified:
                session.modified = True
            vals_count += 1
            calc_extrasensory_level(int(myvalue))

        ext_accuracy, ext_vals = get_extrasensory_data()
        return render_template('result.html',
                               vals_count=vals_count,
                               myvals=session.get('myvals', []),
                               ext_accuracy=ext_accuracy,
                               ext_vals=ext_vals)
    else:
        vals_count = len(session.get('myvals', []))
        num = session.get('num', 0)
        print(vals_count)
        print(num)
        if vals_count == num:
            extrasensory_predict()
        exp_resp = get_extrasensory_value()
        return render_template('input_val.html', form=form, exp_resp=exp_resp)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return redirect(url_for('input_val'))
    elif request.method == 'GET':
        num = session.get('num', 0)
        if num == 0:
            session['myvals'] = []
            for i in range(extrasensory_count):
                session[f'ext_accuracy:{i}'] = 0
                session[f'ext_vals:{i}'] = []

        vals_count = len(session.get('myvals', []))
        ext_accuracy, ext_vals = get_extrasensory_data()

        return render_template('index.html',
                               vals_count=vals_count,
                               myvals=session.get('myvals', []),
                               ext_accuracy=ext_accuracy,
                               ext_vals=ext_vals)


if __name__ == '__main__':
    app.run()
