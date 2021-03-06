from flask import Flask
from flask import render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import time
from datetime import datetime
import config
import hashlib

app = Flask(__name__)
app.config['SECRET_KEY'] = config.secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def verify_password(self, password):
        return self.password == hash_password(password)

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    author = db.Column(db.String)
    topic = db.Column(db.String)
    title = db.Column(db.String(30), nullable = False)
    content = db.Column(db.String, nullable = False)
    picture = db.Column(db.String(48), nullable = True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def index():
    if 'username' in session:
        username = session['username']
        return render_template('index.html', username=username)
    return "You are not logged in <br><a href = '/login'>" + "click here to log in</a>"


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        data = request.form
        user = User(username=data['username'], password=hash_password(data['password']))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('register'))
        return render_template('register.html')
    elif request.method == "GET":
        #user = User.query.first()
        return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        data = request.form
        user = User.query.filter_by(username=data['username'], password=hash_password(data['password'])).first()
        if not user:
            return "asdf"

        session['username'] = data['username']

        return redirect(('/'))
    elif request.method == "GET":
        return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/post', methods = ['GET', 'POST'])
def new_post():

	if request.method == "POST": 
		data = request.form
		
		post = Post(
			   author = session['username']	,	
			   topic = data['topic'],
			   title = data['title'],
			   content = data['content'],
			   picture = data['picture'],		
			)
		
		db.session.add(post)
		db.session.commit()
		
		return render_template("index.html")
	
	else:
	
		return render_template("create_post.html")


if __name__ == '__main__':
	db.create_all()
	app.run(debug=True)
	
