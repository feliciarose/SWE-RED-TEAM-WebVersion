from flask import Flask, render_template, request, redirect, url_for
from incollege import InCollegeApp

app = Flask(__name__)
incollege_app = InCollegeApp()

@app.route('/create_account', methods=['POST'])
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

if __name__ == '__main__':
    app.run(debug=True)
