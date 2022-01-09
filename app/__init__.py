from main_app import app
from views.index import IndexView
from views.hidden_number import HiddenNumberView

app.add_url_rule('/', view_func=IndexView.as_view('index'))
app.add_url_rule('/hidden-number', view_func=HiddenNumberView.as_view('hidden_number'))

application = app

if __name__ == '__main__':
    try:
        app.run()
    except KeyboardInterrupt:
        pass
