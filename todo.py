from flask import Flask
from flask import render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'




db = SQLAlchemy(app)

class Task(db.Model):
    task_id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    desc = db.Column(db.String(200),nullable = False)
    completed = db.Column(db.Boolean,default = False)



@app.route("/")
def index():

    todos = Task.query.filter_by(completed=False).all()
    done = Task.query.filter_by(completed = True).all()

    return render_template('index.html',todos = todos,done=done)


@app.route("/create", methods=['GET','POST'])
def add():

    todo = Task(title= request.form.get('title'),desc = request.form.get('desc'))
    db.session.add(todo)
    db.session.commit()


    return redirect(url_for('index'))


@app.route("/update/<int:task_id>", methods=['GET','POST'])
def update(task_id):

    todo = Task.query.filter_by(task_id = task_id).first()
    todo.completed = True
    print(todo)
    db.session.commit()

    return redirect(url_for('index'))
@app.route("/delete/<int:task_id>", methods=['GET','POST'])
def delete(task_id):

    todo = Task.query.filter_by(task_id = task_id).first()
    db.session.delete(todo)
    db.session.commit()

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
