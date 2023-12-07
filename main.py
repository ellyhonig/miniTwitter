from surfer import Surfer
from flask import Flask, request, render_template, redirect, url_for, flash
from login_manager import LoginManager
from profile_manager import ProfileManager
from super_user import SuperUser
from application_manager import ApplicationManager
from warning_manager import WarningManager
from tweet_manager import TweetManager
from job_manager import JobManager
import os
import csv

app = Flask(__name__)
app.secret_key = 'secretkey'
logged_in = [1]
db_accounts = []
db_tweets = []
info = [""]
'''message, author, likes, dislikes'''

login_manager = LoginManager()  # currently logged in user's info
profile_manager = ProfileManager(login_manager)  # edits profiles.csv
application_manager = ApplicationManager()  # edits register.csv
warning_manager = WarningManager()  # edits warnings.csv
super_user = SuperUser(profile_manager, application_manager, warning_manager)
tweet_manager = TweetManager(login_manager=login_manager, warning_manager=warning_manager, profile_manager=profile_manager)
job_manager = JobManager(profile_manager=profile_manager)


@app.route('/')
def homepage():
    trendyusers = profile_manager.get_trendyusers()
    tweets = tweet_manager.get_trendytweets()
    for tweet in tweets:
        tweet['likes'] = tweet_manager.count_likes(tweet['liker_list'])

    if trendyusers is None:
        return render_template('home.html', tweets = tweets[:3], trendyusers = ['None'])
    else:
        return render_template('home.html', tweets = tweets[:3], trendyusers = trendyusers)

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

    if success:
        # Check for temp password or more than 3 warnings
        if password == "temp" or warning_manager.count_warnings(username) > 3:
            return redirect(url_for('payments_page'))

        # Redirect based on user type
        user_type = login_manager.current_user['user_type']
        redirect_func = user_type_redirect.get(user_type, user_type_redirect['default'])
        return redirect_func()
    else:
        flash(message)
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
    username = login_manager.current_user['username']
    profile_info = profile_manager.get_profile_info(username, warning_manager)
    return render_template('myprofile.html', profile_info=profile_info)
@app.route('/dispute_warnings')
def dispute_warnings():
    username = login_manager.current_user['username']
    warnings = warning_manager.get_user_warnings(username)
    return render_template('dispute_warnings.html', warnings=warnings)

@app.route('/dispute_warning/<int:warning_index>', methods=['POST'])
def dispute_warning(warning_index):
    username = login_manager.current_user['username']
    success, message = warning_manager.dispute_warning(username, warning_index)
    flash(message)
    return redirect(url_for('dispute_warnings'))


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

@app.route('/tweets', methods=['GET', 'POST'])
def tweets_page():
    if request.method == 'POST':
        content = request.form['content']
        keywords = request.form['keywords']
        success, message = tweet_manager.post_tweet(content, keywords)
        flash(message)
        if not success:
            return redirect(url_for('tweets_page'))

    tweets = tweet_manager.get_all_tweets()
    for tweet in tweets:
        tweet['likes'] = tweet_manager.count_likes(tweet['liker_list'])
    return render_template('tweets.html', tweets=tweets)

    
@app.route('/like_tweet/<int:tweet_index>', methods=['POST'])
def like_tweet(tweet_index):
    tweet_manager.like_tweet(tweet_index, login_manager.current_user['username'])
    return redirect(url_for('tweets_page'))

@app.route('/dislike_tweet/<int:tweet_index>', methods=['POST'])
def dislike_tweet(tweet_index):
    tweet_manager.dislike_tweet(tweet_index, login_manager.current_user['username'])
    return redirect(url_for('tweets_page'))

@app.route('/complain_tweet/<int:tweet_index>', methods=['POST'])
def complain_tweet(tweet_index):
    tweet_manager.complain_tweet(tweet_index)
    return redirect(url_for('tweets_page'))

@app.route('/comment_tweet/<tweet_index>', methods=['POST'])
def comment_tweet(tweet_index):
    comment = request.form['comment']
    username = login_manager.current_user['username']
    tweet_manager.comment_tweet(tweet_index, comment, username)
    return redirect(url_for('tweets_page'))
@app.route('/tip_tweet/<author>', methods=['POST'])
def tip_tweet(author):
    tip_amount = 1  
    tipper_username = login_manager.current_user['username']

    success, message = profile_manager.tip_user(tipper_username, author, tip_amount)
    flash(message)
    return redirect(url_for('tweets_page'))  

@app.route('/administrative')
def administrative_page():
    return render_template('administrative.html')

@app.route('/user-management')
def user_management():
    users = profile_manager.get_all_profiles()
    return render_template('user_management.html', users=users)

@app.route('/warn_user/<username>', methods=['POST'])
def warn_user(username):
    accuser = 'superuser' 
    warning_manager.add_warning(username, accuser)
    flash(f"Warning issued to {username}.")
    return redirect(url_for('user_management'))

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
@app.route('/disputes')
def disputes():
    disputed_warnings = warning_manager.get_disputed_warnings()
    return render_template('disputes.html', disputed_warnings=disputed_warnings)

@app.route('/remove-warning/<accused_user>/<accuser_user>', methods=['POST'])
def remove_warning(accused_user, accuser_user):
    super_user.remove_warning(accused_user, accuser_user)
    return redirect(url_for('disputes'))    
@app.route('/payments')
def payments_page():
    return render_template('payments.html')

@app.route('/change_password', methods=['POST'])
def change_password():
    new_password = request.form['new_password']
    username = login_manager.current_user['username']
    profile_manager.change_password(username, new_password)
    return redirect(url_for('homepage'))

@app.route('/deposit', methods=['POST'])
def deposit():
    username = login_manager.current_user['username']
    profile_manager.update_balance(username, 10, add=True)
    return redirect(url_for('payments_page'))

@app.route('/pay_fine', methods=['POST'])
def pay_fine():
    username = login_manager.current_user['username']
    balance = profile_manager.get_balance(username)
    if balance >= 10:
        profile_manager.update_balance(username, 10, add=False)
        warning_manager.remove_all_warnings(username)
        # Redirect with a success message
        flash("Fine paid successfully.")
    else:
        # Redirect with an error message
        flash("Insufficient balance to pay the fine.")
    return redirect(url_for('payments_page'))
@app.route('/delete_profile', methods=['POST'])
def delete_profile():
    username = login_manager.current_user['username']
    profile_manager.delete_profile(username)
    return redirect(url_for('homepage'))    



@app.route('/jobs', methods=['GET', 'POST'])
def jobs_page():
    user_type = login_manager.current_user['user_type']  # Define user_type for both GET and POST requests

    if request.method == 'POST':
        message = request.form['message']
        success, response_message = job_manager.post_job(message, login_manager.current_user['username'], user_type)
        flash(response_message)
        if not success:
            return redirect(url_for('jobs_page'))

    jobs = job_manager.get_all_jobs()
    return render_template('jobs.html', jobs=jobs, user_type=user_type)
@app.route('/post_job', methods=['POST'])
def post_job():
    message = request.form['message']
    user_type = login_manager.current_user['user_type']
    author = login_manager.current_user['username']
    success, response_message = job_manager.post_job(author, message, user_type)
    flash(response_message)
    return redirect(url_for('jobs_page'))

@app.route('/apply_job/<int:job_index>', methods=['POST'])
def apply_job(job_index):
    applicant = login_manager.current_user['username']
    success, response_message = job_manager.apply(job_index, applicant)
    flash(response_message)
    return redirect(url_for('jobs_page'))    