from surfer import Surfer
from flask import Flask, request, render_template, redirect, url_for, flash
from login_manager import LoginManager
from profile_manager import ProfileManager
from super_user import SuperUser
import os
import csv

app = Flask(__name__)
app.secret_key = 'secretkey'
logged_in = [1]
db_accounts = []
db_tweets = []
info = [""]
'''message, author, likes, dislikes'''

login_manager = LoginManager()
profile_manager = ProfileManager(login_manager)
super_user = SuperUser(profile_manager)

@app.route('/')
def homepage():
    return render_template('home.html')

def redirect_super_user():
    return redirect(url_for('administrative_page'))

def redirect_other_user():
    return redirect(url_for('homepage'))

# Dictionary for redirect on login
user_type_redirect = {
    'SuperUser': redirect_super_user,
    
    'default': redirect_other_user,
}

@app.route('/login')
def loginPage():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    message, success = login_manager.login(username, password)
    flash(message)
    if success:
        user_type = login_manager.current_user['user_type']
        # Get the redirect function based on user type or use default
        redirect_func = user_type_redirect.get(user_type, user_type_redirect['default'])
        return redirect_func()
    else:
        return render_template('login.html')

@app.route('/register')
def registerPage():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def apply_post():
    desired_username = request.form['username']
    surfer = Surfer()
    surfer.submit_application(desired_username)
    return homepage()


    

@app.route('/myprofile')
def profilePage():
    return render_template('myprofile.html')


@app.route('/myprofileChange')
def profilePageChanges():
    return render_template('myprofileChange.html')

@app.route('/myprofileChange', methods = ['POST'])
def profilePageChanges_post():
    info[0] = ((request.form['profilename'], request.form['birthday'], request.form['location']))
    return render_template('myprofile.html', info = info)

@app.route('/application-manager')
def application_manager():
    applications = []
    with open('registration.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            applications.append(row)
    return render_template('application_manager.html', applications=applications)
    
@app.route('/tweets')
def tweetsPage():
    return render_template('tweets.html', db_tweets = db_tweets)

@app.route('/tweets', methods = ['POST'])
def tweetsPage_post():
    '''form = Message(request.form)'''
    db_tweets.append((request.form['message'], logged_in[0], 0, 0))
    return render_template('tweets.html', db_tweets = db_tweets)

@app.route('/administrative')
def administrative_page():
    return render_template('administrative.html')  