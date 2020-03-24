from flask import Flask, render_template

# create a Flask App
todo_app = Flask(__name__)

# show a list of Todos at the homepage


@todo_app.route('/')
def index():
    # render template is used to render html page which by default is expected in templates located
    # in your project directory
    return render_template('index.html', data=[{
        'description': 'Todo 1'
    }, {
        'description': 'Todo 2'
    }, {
        'description': 'Todo 3'
    }])
