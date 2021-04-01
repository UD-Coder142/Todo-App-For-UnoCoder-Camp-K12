from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(2000), nullable=False)

    def __repr__(self):
        return "<Task %r>" % self.id

@app.route('/home', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form.get("todo_task")
        Task = Todo(content=name)

        db.session.add(Task)
        db.session.commit()

        return redirect(url_for('home'))
    else:
        Tasks = Todo.query.order_by(Todo.id)
        return render_template('index.html', todo=Tasks)

@app.route('/tasks/delete/<int:id>', methods=["GET", "POST"])
def delete(id):
    Task = Todo.query.get_or_404(id)

    db.session.delete(Task)
    db.session.commit()

    return redirect(url_for('home'))

@app.route('/tasks/update/<int:id>', methods=["GET", "POST"])
def update(id):
    if request.method == "POST":
        name = request.form.get("todo_task")
        Task = Todo.query.get_or_404(id)

        Task.content = name
        db.session.commit()

        return redirect(url_for('home'))
    else:
        return render_template("update.html", val=id)

@app.route('/', methods=["GET", "POST"])
def index():
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True) 
