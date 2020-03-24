from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


# create a Flask App
todo_app = Flask(__name__)
# connect to the SQL database todoapp
todo_app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:database@localhost:5433/todoapp'
todo_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# define db object
db = SQLAlchemy(todo_app)


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)


    #create a printing wrapper for better presentation
    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'

#create the entries in the database
db.create_all()

# show a list of Todos at the homepage

@todo_app.route('/')
def index():
    # render template is used to render html page which by default is expected in templates located
    # in your project directory
    return render_template('index.html', data=Todo.query.all())
