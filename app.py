
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
# connect to the SQL database todoapp
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:database@localhost:5433/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

migrate = Migrate(app, db)

class Todo(db.Model):
    __tablename__ = 'todos4'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=False)

def __repr__(self):
    return f'<Todo {self.id} {self.description}>'

class TodoList(db.Model):
    __tablename__ = 'todolists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    todos = db.relationship('Todo', backref='list', lazy=True)

#create the entries in the database
# db.create_all()

# App route to create new ToDo items using our view and controller to update the Model
@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    body = {}
    try:
        description = request.get_json()['description']
        todo = Todo(description=description)
        db.session.add(todo)
        db.session.commit()
        body['description'] = todo.description
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort (400)
    else:
        redirect(url_for('index'))
        return jsonify(body)

# App route used to detect and insert check box true to the database
@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
    try:
        completed = request.get_json()['completed']
        todo = Todo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
        return redirect(url_for('index'))

# App route to delete copleted tasks
@app.route('/todos/<todo_id>/delete-selected', methods=['GET'])
def delete_selected(todo_id):
    try:
        # completed = request.get_json()['completed']
        Todo.query.filter_by(id=todo_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
        redirect(url_for('index'))
        return jsonify({'success': True })


# This is the homepage route
@app.route('/lists/<list_id>')
def get_list_todos(list_id):
  return render_template('index.html',
    lists=TodoList.query.all(),
    todos=Todo.query.filter_by(list_id=list_id).order_by('id').all())

@app.route('/')
def index():
  return redirect(url_for('get_list_todos', list_id=1))