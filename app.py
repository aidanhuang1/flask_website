from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'secretkey'
app.permanet_session_lifetime = timedelta(minutes=5)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        session.permanent = True
        user = request.form['nm']
        # print(user)
        session['user'] = user 
        return redirect(url_for('user'))
    else:
        if 'user' in session:
            return redirect(url_for('user'))
        return render_template('login.html')

@app.route('/user')
def user():
    if 'user' in session:
        user = session['user']
        return f"<h1>{user}</h1>"
    else: #if the user is not in the session, has to login again, etc...
        return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    flash('you have been logged out', 'info')
    session.pop('user', None) #remove user session
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
