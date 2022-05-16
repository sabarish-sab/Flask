from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///list.sqlite3'
app.config['SECRET_KEY'] = 'AS62nsfjadsaj_@dfjfsfhbf182sfjdfASFAKSF'


db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    Date = db.Column(db.String)
    Name = db.Column(db.String(100))
    Email = db.Column(db.String(100), unique=True, nullable=True)
    Phone = db.Column(db.String(100), unique=True, nullable=True)
    Priority = db.Column(db.String(100))

    def __init__(self, date, name, email, phone, pri):
        self.Date = date
        self.Name = name
        self.Email = email
        self.Phone = phone
        self.Priority = pri


@app.route('/')
def index():
    return render_template('index.html')


msg=None


@app.route('/add', methods=['GET', 'POST'])
def add():
    msg = None
    if request.method == 'POST':
        try:
            list = Todo(
                request.form['t_date'], request.form['t_name'], request.form['t_email'], request.form['t_phone'], request.form['t_pri'])
            db.session.add(list)
            db.session.commit()

            msg = "Your task added successfully"
            return render_template('index.html', msg=msg)
        except:
            msg = 'OOPS something went wrong task not added, TRY AGAIN!'
            return render_template('index.html', msg=msg)

    return render_template('index.html', msg=msg)


@app.route('/list')
def list():
    return render_template('list.html', lists=Todo.query.all())


@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    list = Todo.query.filter_by(id=id).first()

    if request.method == 'POST':
        try:
            list.Task_Date = request.form['date']
            list.Task_Name = request.form['name']
            list.Task_Email = request.form['email']
            list.Task_Phone = request.form['phone']
            list.Task_Priority = request.form['pri']

            db.session.commit()
            msg = 'This task is updated successfully'
            return render_template('edit.html', msg=msg, list=list)
        except:
            msg = 'OOPS something went wrong task not updated, TRY AGAIN!'
            return render_template('edit.html', msg=msg, list=list)
    else:
        return render_template('edit.html', list=list)


@app.route('/delete/<id>')
def delete(id):
    try:
        Todo.query.filter_by(id=id).delete()
        db.session.commit()
        msg = 'This task is Deleted successfully'
        return render_template('list.html', msg=msg, lists=Todo.query.all())
    except:
        flash('OOPS something went wrong task not deleted, TRY AGAIN!')

    return redirect(url_for('index'))



if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)