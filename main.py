from surfer import Surfer
from flask import Flask, request, render_template, redirect, url_for, flash
from login_manager import LoginManager
from profile_manager import ProfileManager
from super_user import SuperUser
from application_manager import ApplicationManager
import os
import csv

app = Flask(__name__)
app.secret_key = 'secretkey'
logged_in = [1]
db_accounts = []
db_tweets = []
info = [""]
'''message, author, likes, dislikes'''

login_manager = LoginManager() #contains currently logged in user's info
profile_manager = ProfileManager(login_manager) #edits profiles.csv
application_manager = ApplicationManager()
super_user = SuperUser(profile_manager, application_manager)


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



@app.route('/register', methods=['GET', 'POST'])
def registerPage():
    if request.method == 'POST':
        desired_username = request.form['username']
        user_type = request.form['user_type']
        surfer = Surfer()
        surfer.submit_application(desired_username, user_type)
        return redirect(url_for('registerPage'))
    return render_template('register.html')
@app.route('/check-status', methods=['POST'])
def check_status():
    username = request.form['check_username']
    surfer = Surfer()
    status, rejection_reason, temp_password = surfer.check_application_status(username)
    return render_template('status.html', status=status, rejection_reason=rejection_reason, temp_password=temp_password)

    

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
def application_manager_page():
    applications = application_manager.get_applications()
    return render_template('application_manager_page.html', applications=applications)
@app.route('/accept-application', methods=['POST'])
def accept_application():
    username = request.form['username']
    temp_password = request.form['temp_password']
    super_user.manage_application(username, accept=True, temp_password=temp_password)
    return redirect(url_for('application_manager_page'))

@app.route('/reject-application', methods=['POST'])
def reject_application():
    username = request.form['username']
    rejection_reason = request.form['rejection_reason']
    super_user.manage_application(username, accept=False, rejection_reason=rejection_reason)
    return redirect(url_for('application_manager_page'))

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

@app.route('/user-management')
def user_management():
    users = profile_manager.get_all_profiles()
    return render_template('user_management.html', users=users)

@app.route('/delete-user/<username>', methods=['POST'])
def delete_user(username):
    super_user.delete_user(username)
    return redirect(url_for('user_management'))    
@app.route('/add-profile', methods=['POST'])
def add_profile():
    username = request.form['username']
    password = request.form['password']
    user_type = request.form['user_type']
    super_user.add_profile(username, password, user_type, '0') 
    return redirect(url_for('user_management'))    