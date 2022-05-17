
# from os import abort
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

@app.route('/')
def index():
    return render_template('index.html',data=Todo.query.all())

