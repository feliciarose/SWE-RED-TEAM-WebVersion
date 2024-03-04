from flask import Flask, render_template, request
from app import app
from incollege import InCollegeApp 

# Instantiate InCollegeApp
incollege_app = InCollegeApp()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_account', methods=['POST'])
def create_account():
    username = request.form.get('username')
    password = request.form.get('password')
    result = incollege_app.create_account(username, password)
    return result
