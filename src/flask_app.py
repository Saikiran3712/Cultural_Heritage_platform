# Clean Flask Application
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email
import requests
import os
from datetime import datetime
import uuid

# Configuration
API_BASE_URL = "https://api.corpus.swecha.org/api/v1"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cultural-heritage-platform-secret-key-2025'
app.config['WTF_CSRF_ENABLED'] = False

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # type: ignore

class User(UserMixin):
    def __init__(self, user_id, phone, name, email, access_token):
        self.id = user_id
        self.phone = phone
        self.name = name
        self.email = email
        self.access_token = access_token

@login_manager.user_loader
def load_user(user_id):
    if 'user_data' in session:
        user_data = session['user_data']
        if user_data['id'] == user_id:
            return User(
                user_data['id'],
                user_data['phone'], 
                user_data['name'],
                user_data['email'],
                user_data['access_token']
            )
    return None

# API Helper Functions
def api_request(endpoint, method='GET', data=None, token=None, form_data=False, files=None):
    """Make API requests to the corpus API"""
    url = f"{API_BASE_URL}{endpoint}"
    headers = {}
    
    if token:
        headers['Authorization'] = f'Bearer {token}'
    
    if not form_data and not files:
        headers['Content-Type'] = 'application/json'
    
    try:
        if method == 'POST':
            if files:
                response = requests.post(url, data=data, files=files, headers=headers, timeout=60)
            elif form_data:
                response = requests.post(url, data=data, headers=headers, timeout=30)
            else:
                response = requests.post(url, json=data, headers=headers, timeout=10)
        elif method == 'GET':
            response = requests.get(url, headers=headers, params=data, timeout=10)
        else:
            return None
            
        return response
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return None

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@app.route('/content')
@login_required  
def content():
    return render_template('content.html')

@app.route('/my-records')
@login_required
def my_records():
    return render_template('my_records.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)