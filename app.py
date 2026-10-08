from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db=SQLAlchemy(app)

class Todo(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/', methods=['GET', 'POST'])
def index():
    # return "Hello, World"
    if request.method == 'POST':
        # Get from HTML name='content'
        task_content = request.form['content']
        # Build model
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f"There was an issue adding your task: {e}"
    else:
        # Fetch from dB
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)
    # return render_template('index.html', name='Dhairya')

@app.route('/delete/<int:id>')
def delete_task(id):
    task_to_delete = db.get_or_404(Todo, id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return f"Could not delete task: {e}"

@app.route('/update/<int:id>')
def update_task(id):
    task_to_update = db.get_or_404(Todo, id) 
    try:
        task_to_update.completed = 0 if task_to_update.completed == 1 else 1
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return f"Could not update task: {e}"

if __name__ == '__main__':
    app.run(debug=True)