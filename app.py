from flask import Flask, render_template,request,redirect
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
Scss(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db = SQLAlchemy(app)

class Mytask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"Task {self.id}"

with app.app_context():
        db.create_all()

@app.route("/", methods=["POST",'GET'])
def index():
    #add task
    if request.method == "POST":
        current_task = request.form['todo']
        new_task = Mytask(todo=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(f"Error:{e}")
            return f"Error:{e}"
    else:
        tasks = Mytask.query.order_by(Mytask.created).all()
        completed_count = Mytask.query.filter_by(completed=1).count()
        return render_template("index.html", tasks=tasks,completed_count=completed_count)
    
#delete an item
@app.route("/delete/<int:id>")
def delete(id:int):
    delete_task = Mytask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"ERROR : {e}"
    

# Edit a task
@app.route("/edit/<int:id>", methods=["POST"])
def edit(id):
    task = Mytask.query.get_or_404(id)
    task.todo = request.form['todo']
    try:
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"ERROR: {e}"
    
# Toggle a task
@app.route("/toggle/<int:id>")
def toggle(id):
    task = Mytask.query.get_or_404(id)

    # Toggle between 0 and 1
    task.completed = not task.completed
    try:
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"ERROR: {e}"

if __name__ == "__main__":
    app.run(debug=True)