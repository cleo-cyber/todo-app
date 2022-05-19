
# from crypt import methods
import sys
# from unicodedata import name
from flask import Flask, render_template, request,redirect,url_for,jsonify,abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:Cleo1999*@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)
migrate= Migrate(app, db)

class Todo(db.Model):
    __tablename__='todos'
    id=db.Column(db.Integer,primary_key=True)
    decription=db.Column(db.String(),nullable=False)
    completed=db.Column(db.Boolean,default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=False)
    
    def __repr__(self):
        return f'<Todo {self.id} {self.description}> '
    
    
class TodoList(db.Model):
        __tablename__ = 'todolists'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(), nullable=False)
        todos = db.relationship('Todo', backref='list', lazy=True)

        def __repr__(self):
            return f'<TodoList {self.id} {self.name}>'

order_items = db.Table('order_items',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
)

class Order(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  status = db.Column(db.String(), nullable=False)
  products = db.relationship('Product', secondary=order_items,
      backref=db.backref('orders', lazy=True))

class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(), nullable=False)
  
  
@app.route('/todolists/create',methods=['POST'])
def create_todo_lists():
    name=request.get_json()['create']
    newlist=TodoList(name=name)
    db.session.add(newlist)
    db.session.commit()
    redirect(url_for('get_list_todos'))

@app.route('/todos/create',methods=['POST'])
def create_todo():
    error=False
    body={}
    
    try:
        # decription=request.form.get('decription','')
        decription=request.get_json()['description']
        # print('completed', completed)
        todo=Todo(decription=decription,completed=False)
        body['completed']=todo.completed
        db.session.add(todo)
        db.session.commit()
        # return redirect(url_for('index'))
        # body['description']=todo.decription   

    except:
        error=True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
        if error==True:
           abort(400)
        else:
            return jsonify(body)


@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
    try:
        completed=request.get_json('completed')
        todo=Todo.query.get(todo_id)
        todo.completed=completed
        # db.session.add(todo.completed)
        db.session.commit()

    except:
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
        return redirect(url_for('index'))
    
    
@app.route('/todos/<delete_id>',methods=['DELETE'])
def delete_todo(delete_id):
    try:
        # delete=Todo.id
        Todo.query.filter_by(id=delete_id).delete()
    #    Todo.query.filter_by(id=delete_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
        return jsonify({'success':True})


@app.route('/lists/<list_id>')
def get_list_todos(list_id):
    return render_template('index.html',
            lists=TodoList.query.all(), 
            active_list=TodoList.query.get(list_id),      
            todos=Todo.query.filter_by(list_id=list_id).order_by('id').all())


@app.route('/')
def index():
    return redirect(url_for('get_list_todos',list_id=1))
