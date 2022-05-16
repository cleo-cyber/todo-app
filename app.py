# from crypt import methods
# from sre_parse import FLAGS
from crypt import methods
from flask import Flask, render_template, request
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

@app.route('/create',methods=['POST'])
def create_todo():
    decription=request.form.get('decription','')
    todo=Todo(decription=decription)
    db.session.add(todo)
    db.session.commit()
    

@app.route('/')
def index():
    return render_template('index.html',data=Todo.query.all())

