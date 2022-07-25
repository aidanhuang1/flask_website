from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from second import second
import pyrebase

app = Flask(__name__)

config = {
    'apiKey': "AIzaSyCghngurNTrJ4jlLcxe5cvLFLr7frvN6V8",
    'authDomain': "authentication-flask-website.firebaseapp.com",
    'projectId': "authentication-flask-website",
    'storageBucket': "authentication-flask-website.appspot.com",
    'messagingSenderId': "671826927467",
    'appId': "1:671826927467:web:24ce92e9ddd9d0377b362e",
    'measurementId': "G-T48NEMQW4M",
    'databaseURL': ''
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

app.register_blueprint(second, url_prefix="")
app.secret_key = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=5)

db=SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    
    def __init__(self, name, email):
        self.name = name
        self.email = email
        
@app.before_first_request
def create_tables():
    db.create_all()
    
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/view')
def view():
    return render_template('view.html', values=users.query.all())

@app.route("/login", methods=['GET', 'POST'])
def login():
    if 'user' in session:
        flash("Already logged in")
        return redirect(url_for('user'))
    if request.method == 'POST':
        session.permanent = True
        # user = request.form['nm']
        # session['user'] = user 
        
        # found_user = users.query.filter_by(name=user).first()
        # if found_user: 
        #     #user is found in database
        #     session['email'] = found_user.email
        # else: 
        #     #if user doesn't exist in database
        #     usr = users(user, '')
        #     db.session.add(usr)
        #     db.session.commit()
        email = request.form.get('email')
        password = request.form.get('password') 
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = email
            print(user)
            
            flash('login successful!')
            return redirect(url_for('user'))
        except:
            flash('failed to login')        
    
    return render_template('login.html')

@app.route('/user', methods=['POST', 'GET'])
def user():
    email = None
    if 'user' in session:
        user = session['user']        
        if request.method == 'POST':
            email = request.form['email']
            session['email'] = email
            found_user = users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit()
            flash('email has been saved!')
        else:
            if 'email' in session:
                email = session['email']
        return render_template('user.html', email=email)
    else: #if the user is not in the session, has to login again, etc...
        flash('you are not logged in!')
        return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    flash('you have been logged out', 'info')
    session.pop('user', None) #remove user session
    session.pop('email', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    db.create_all()#create database if it doesn't exist already
    app.run(debug=True)
