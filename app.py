
# from os import abort

# from crypt import methods
import sys
from flask import Flask, render_template, request,redirect,url_for,jsonify,abort
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:Cleo1999*@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)

class Todo(db.Model):
    __tablename__='todos'
    id=db.Column(db.Integer,primary_key=True)
    decription=db.Column(db.String(),nullable=False)
    # completed=db.Column(db.Boolean,nullable=False)
    
    def __repr__(self):
        return f'<Todo {self.id} {self.description}> '
    
db.create_all()

@app.route('/todos/create',methods=['POST'])
def create_todo():
    error=False
    body={}
    
    try:
        # decription=request.form.get('decription','')
        decription=request.get_json()['description']
        todo=Todo(decription=decription)
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
    
@app.route('/')
def index():
    return render_template('index.html',data=Todo.query.order_by('id').all())

