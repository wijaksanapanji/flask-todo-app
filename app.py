from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=0)

    def __repr__(self):
        return '<Todo %r>' % self.id


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        todo = request.form['todo']
        new_todo = Todo(todo=todo)
        try:
            db.session.add(new_todo)
            db.session.commit()
            return redirect('/')
        except:
            return 'Failed adding todo, there\'s something wrong!'
    else:
        todos = Todo.query.order_by(Todo.created_at).all()
        return render_template('index.html', todos=todos)


if __name__ == "__main__":
    app.run(debug=True)
