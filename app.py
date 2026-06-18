from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    status = db.Column(db.String(20), default="active")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/tasks')
def tasks():
    all_tasks = Task.query.all()
    return render_template('tasks.html', tasks=all_tasks)

@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    new_task = Task(title=title)
    db.session.add(new_task)
    db.session.commit()
    return redirect('/tasks')

@app.route('/delete/<int:id>')
def delete(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return redirect('/tasks')

@app.route('/done/<int:id>')
def done(id):
    task = Task.query.get(id)
    task.status = "done"
    db.session.commit()
    return redirect('/tasks')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/dashboard')
def dashboard():
    total = Task.query.count()
    done = Task.query.filter_by(status="done").count()
    active = total - done
    return render_template('dashboard.html', total=total, done=done, active=active)

@app.route('/contact')
def contact():
    return render_template('contact.html')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)