from flask import Flask, render_template, request, redirect, url_for
from incollege import InCollegeApp

app = Flask(__name__)
incollege_app = InCollegeApp()


@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')

        # Call the create_account method from InCollegeApp
        result = incollege_app.create_account(username, password, first_name, last_name)
        if "Account created successfully" in result:
            return render_template('login.html', message=incollege_app.translate_language(result))
        else:
            return render_template('create_account.html', error=incollege_app.translate_language(result))
    else:
        return render_template('create_account.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if incollege_app.login(username, password):
            # Redirect to home_page.html upon successful login
            return redirect(url_for('home_page'))
        else:
            error_message = "Incorrect username or password"
            return render_template('login.html', error=error_message)
    else:
        return render_template('login.html')

@app.route('/home_page')
def home_page():
    return render_template('home_page.html')

# ----------------------- epic 5 -----------------------#

# ------------------ task4 ----------------

@app.route('/create_profile', methods=['GET', 'POST'])
def create_profile():
    if request.method == 'POST':
        # Retrieve form data
        username = request.form.get('username')
        profile_title = request.form.get('profile_title')
        major = request.form.get('major')
        university = request.form.get('university')
        about = request.form.get('about')
        experience = request.form.get('experience')
        education = request.form.get('education')
        
        # Save profile data in the profiles dictionary
        incollege_app.create_profile(username, profile_title, major, university, about, experience, education)
        
        # Redirect to the user's profile page
        return redirect(url_for('view_profile', username=username))
    else:
        # Handle GET requests to this route (optional)
        return render_template('create_profile.html')


@app.route('/view_profile/<username>', methods=['GET'])
def view_profile(username):
    profile = incollege_app.view_profile(username)
    return render_template('view_profile.html', profile=profile)


@app.route('/post_login_options')
def post_login_options():
    # Logic to handle post login options goes here
    return render_template('post_login_options.html')  # Assuming 'post_login_options.html' is your main menu template


# ----------------------- epic 6 -----------------------#

@app.route('/job_search', methods=['GET'])
def job_search():
    company = request.args.get('company')
    role = request.args.get('role')
    experience_level = request.args.get('experience_level')

    # Perform job search with the provided filters
    filtered_jobs = incollege_app.job_search(company, role, experience_level)
    
    # Check if there are any jobs available
    if not filtered_jobs:
        return render_template('no_jobs.html')  # Render a template indicating no jobs available

    return render_template('display_jobs.html', jobs=filtered_jobs)


@app.route('/post_job', methods=['GET', 'POST'])
def post_job():
    if request.method == 'POST':
        # Extract job details from the form
        title = request.form['title']
        description = request.form['description']
        employer = request.form['employer']
        location = request.form['location']
        salary = request.form['salary']
        role = request.form['role']
        experience_level = request.form['experience_level']

        # Call the post_job function from InCollegeApp
        result = incollege_app.post_job(title, description, employer, location, salary, role, experience_level)
        
        # Render the post job result template with the result message
        return render_template('post_job_result.html', message=result)
    else:
        # Render the post job form template
        return render_template('post_job.html')

@app.route('/apply_for_job', methods=['POST'])
def apply_for_job():
    if request.method == 'POST':
        # Extract job details from the form
        job_title = request.form['job_title']
        job_description = request.form['job_description']
        employer = request.form['employer']
        location = request.form['location']
        salary = request.form['salary']
        role = request.form['role']
        experience_level = request.form['experience_level']

        username = request.form.get('username')

        # Call the apply_for_job function from InCollegeApp
        job = incollege_app.apply_for_job(username, job_title, job_description, employer, location, salary, role, experience_level)

        # Redirect to a page indicating successful application
        return render_template('apply_for_job.html', message=job)

@app.route('/applied_sucessfully', methods=['GET', 'POST'])
def applied_successfully():
    if request.method == 'POST':
        # Handle POST request here (if needed)
        return render_template('applied_sucessfully.html')  # Render the template or perform other actions
    else:
        # Handle GET request here
        return render_template('applied_sucessfully.html')  # Render the template or perform other actions

@app.route('/job_saved', methods=['POST'])
def save_job():
    if request.method == 'POST':
        # Extract job details from the form
        job_title = request.form['job_title']
        job_description = request.form['job_description']
        employer = request.form['employer']
        location = request.form['location']
        salary = request.form['salary']
        role = request.form['role']
        experience_level = request.form['experience_level']

        username = request.form.get('username')

        # Call the save_job function from InCollegeApp
        job = incollege_app.save_job(username, job_title, job_description, employer, location, salary, role, experience_level)

        # Redirect to job saved page
        return render_template('/job_saved.html', message=job)

# ----------------------- epic 7 -----------------------#

@app.route('/user_tier_check', methods=['GET', 'POST'])
def user_tier_check():
    user_tiers = incollege_app.get_user_tier('username')
    if request.method == 'POST':
        username = request.form['username']
        if username in user_tiers:
            tier = user_tiers[username]
            return render_template('tier_status.html', username=username, tier=tier, show_upgrade=True)
        else:
            message = "User tier not found."
            return render_template('user_tier_check.html', message=message)
    return render_template('user_tier_check.html')


messages = []

@app.route('/message')
def message_management():
    new_msg_count = len([msg for msg in messages if not msg['read'] and msg['recipient'] == 'username'])
    return render_template('message_management.html', new_msg_count=new_msg_count)

@app.route('/send-message', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        recipient = request.form['recipient']
        message = request.form['message']
        messages.append({
            'sender': 'username',
            'recipient': recipient,
            'message': message,
            'read': False
        })
        return redirect(url_for('message_management'))
    else:
        return render_template('send_message.html')

@app.route('/view-messages')
def view_messages():
    user_messages = [msg for msg in messages if msg['recipient'] == 'username']
    for msg in user_messages:
        msg['read'] = True
    return render_template('view_messages.html', user_messages=user_messages)


if __name__ == '__main__':
    app.run(debug=True)
