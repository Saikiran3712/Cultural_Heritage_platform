# Pure API-based Flask Application
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email
import requests
import os
from datetime import datetime
import uuid
from io import BytesIO

# Configuration
API_BASE_URL = "https://api.corpus.swecha.org/api/v1"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cultural-heritage-platform-secret-key-2025'
app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for API integration

# Language support
LANGUAGES = {
    'en': 'English',
    'te': 'తెలుగు (Telugu)',
    'hi': 'हिंदी (Hindi)',
    'ta': 'தமிழ் (Tamil)',
    'bn': 'বাংলা (Bengali)',
    'mr': 'मराठी (Marathi)',
    'gu': 'ગુજરાતી (Gujarati)',
    'kn': 'ಕನ್ನಡ (Kannada)',
    'ml': 'മലയാളം (Malayalam)',
    'pa': 'ਪੰਜਾਬੀ (Punjabi)',
    'or': 'ଓଡ଼ିଆ (Odia)',
    'ur': 'اردو (Urdu)',
    'as': 'অসমীয়া (Assamese)'
}

TRANSLATIONS = {
    'en': {
        'cultural_heritage_platform': 'Cultural Heritage Platform',
        'dashboard': 'Dashboard',
        'submit_content': 'Submit Content',
        'my_records': 'My Records',
        'profile': 'Profile',
        'logout': 'Logout',
        'login': 'Login',
        'register': 'Register',
        'home': 'Home',
        'welcome': 'Welcome to Cultural Heritage Platform',
        'preserve_culture': 'Preserving India\'s Rich Cultural Heritage',
        'phone_number': 'Phone Number',
        'password': 'Password',
        'full_name': 'Full Name',
        'email': 'Email',
        'title': 'Title',
        'content': 'Content',
        'language': 'Language',
        'location': 'Location',
        'submit': 'Submit',
        'category': 'Category'
    },
    'te': {
        'cultural_heritage_platform': 'సాంస్కృతిక వారసత్వ వేదిక',
        'dashboard': 'డాష్‌బోర్డ్',
        'submit_content': 'కంటెంట్ సమర్పించండి',
        'my_records': 'నా రికార్డులు',
        'profile': 'ప్రొఫైల్',
        'logout': 'లాగ్ అవుట్',
        'login': 'లాగిన్',
        'register': 'నమోదు చేసుకోండి',
        'home': 'హోమ్',
        'welcome': 'సాంస్కృతిక వారసత్వ వేదికకు స్వాగతం',
        'preserve_culture': 'భారతదేశ సమృద్ధ సాంస్కృతిక వారసత్వాన్ని పరిరక్షించడం',
        'phone_number': 'ఫోన్ నంబర్',
        'password': 'పాస్‌వర్డ్',
        'full_name': 'పూర్తి పేరు',
        'email': 'ఇమెయిల్',
        'title': 'శీర్షిక',
        'content': 'కంటెంట్',
        'language': 'భాష',
        'location': 'స్థానం',
        'submit': 'సమర్పించండి',
        'category': 'వర్గం'
    }
}

def get_current_language():
    return session.get('language', 'te')  # Default to Telugu

def translate(key):
    language = get_current_language()
    return TRANSLATIONS.get(language, {}).get(key, TRANSLATIONS['en'].get(key, key))

@app.context_processor
def utility_processor():
    return dict(translate=translate, get_current_language=get_current_language, languages=LANGUAGES)

@app.route('/set-language/<lang_code>')
def set_language(lang_code):
    if lang_code in LANGUAGES:
        session['language'] = lang_code
    return redirect(request.referrer or url_for('index'))

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # type: ignore
login_manager.login_message = 'Please log in to access this page.'

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
    
    # Don't set Content-Type for multipart uploads (requests will set it automatically)
    if not form_data and not files:
        headers['Content-Type'] = 'application/json'
    
    # Debug logging for file uploads
    if files:
        print(f"Making file upload request to {url}")
        print(f"Data: {data}")
        print(f"Files: {list(files.keys()) if files else None}")
    try:
        if method == 'POST':
            if files:
                # For multipart uploads (chunk upload)
                # Increase timeout for file uploads and ensure proper encoding
                response = requests.post(url, data=data, files=files, headers=headers, timeout=60)
            elif form_data:
                # For form data (record finalization)
                response = requests.post(url, data=data, headers=headers, timeout=30)
            else:
                # For JSON data
                response = requests.post(url, json=data, headers=headers, timeout=10)
        elif method == 'PUT':
            if form_data:
                response = requests.put(url, data=data, headers=headers, timeout=30)
            else:
                response = requests.put(url, json=data, headers=headers, timeout=10)
        elif method == 'PATCH':
            if form_data:
                response = requests.patch(url, data=data, headers=headers, timeout=30)
            else:
                response = requests.patch(url, json=data, headers=headers, timeout=10)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers, timeout=10)
        else:
            response = requests.get(url, headers=headers, params=data, timeout=10)
        
        # Log response status for debugging
        if files:
            print(f"Response status: {response.status_code}")
            if response.status_code != 200:
                print(f"Response content: {response.text[:500]}")
            
        return response
    except requests.exceptions.Timeout as e:
        print(f"API request timeout: {e}")
        return None
    except requests.exceptions.ConnectionError as e:
        print(f"API connection error: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {type(e).__name__}: {e}")
        return None

def get_user_token():
    """Get current user's access token"""
    return session.get('user_data', {}).get('access_token')

# Forms
class LoginForm(FlaskForm):
    phone = StringField('Phone Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class UserRegistrationForm(FlaskForm):
    phone = StringField('Phone Number', validators=[DataRequired()])
    name = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Register')

# Routes
@app.route('/')
def index():
    # Get categories from API for homepage
    categories = []
    try:
        response = api_request('/categories/')
        if response and response.status_code == 200:
            categories = response.json()
    except:
        pass
    return render_template('index.html', categories=categories)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        response = api_request('/auth/login', 'POST', {
            'phone': form.phone.data,
            'password': form.password.data
        })
        
        if response and response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get('access_token')
            
            if access_token:
                # Get user info
                user_response = api_request('/auth/me', token=access_token)
                if user_response and user_response.status_code == 200:
                    user_info = user_response.json()
                    
                    user = User(
                        user_info['id'],
                        user_info['phone'],
                        user_info['name'],
                        user_info['email'],
                        access_token
                    )
                    
                    session['user_data'] = {
                        'id': user_info['id'],
                        'phone': user_info['phone'],
                        'name': user_info['name'],
                        'email': user_info['email'],
                        'access_token': access_token
                    }
                    
                    login_user(user)
                    flash('Login successful!', 'success')
                    return redirect(url_for('dashboard'))
        
        flash('Invalid phone number or password', 'error')
    
    return render_template('login.html', form=form)

@app.route('/send-otp', methods=['POST'])
def send_otp():
    json_data = request.json or {}
    phone_number = json_data.get('phone_number')
    
    response = api_request('/auth/login/send-otp', 'POST', {
        'phone_number': phone_number
    })
    
    if response and response.status_code == 200:
        data = response.json()
        return jsonify({
            'success': True, 
            'message': 'OTP sent successfully',
            'reference_id': data.get('reference_id')
        })
    else:
        return jsonify({'success': False, 'message': 'Failed to send OTP'}), 400

@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    json_data = request.json or {}
    phone_number = json_data.get('phone_number')
    otp_code = json_data.get('otp_code')
    
    response = api_request('/auth/login/verify-otp', 'POST', {
        'phone_number': phone_number,
        'otp_code': otp_code
    })
    
    if response and response.status_code == 200:
        token_data = response.json()
        access_token = token_data.get('access_token')
        
        if access_token:
            # Get user info
            user_response = api_request('/auth/me', token=access_token)
            if user_response and user_response.status_code == 200:
                user_info = user_response.json()
                
                user = User(
                    user_info['id'],
                    user_info['phone'],
                    user_info['name'],
                    user_info['email'],
                    access_token
                )
                
                session['user_data'] = {
                    'id': user_info['id'],
                    'phone': user_info['phone'],
                    'name': user_info['name'],
                    'email': user_info['email'],
                    'access_token': access_token
                }
                
                login_user(user)
                return jsonify({'success': True, 'redirect': url_for('dashboard')})
        
        return jsonify({'success': False, 'message': 'Invalid OTP'}), 400
    else:
        return jsonify({'success': False, 'message': 'Invalid OTP'}), 400

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = UserRegistrationForm()
    if form.validate_on_submit():
        response = api_request('/users/', 'POST', {
            'phone': form.phone.data,
            'name': form.name.data,
            'password': form.password.data,
            'has_given_consent': True,
            'role_ids': [2]
        })
        
        if response and response.status_code == 201:
            flash('Registration successful! You can now login.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Registration failed. Please try again.', 'error')
    
    return render_template('register.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    # Get user's contributions from API using the correct endpoint
    user_records = []
    stats = {'total_contributions': 0, 'contributions_by_media_type': {'text': 0, 'audio': 0, 'video': 0, 'image': 0, 'document': 0}}
    
    try:
        response = api_request(f'/users/{current_user.id}/contributions', token=current_user.access_token)
        if response and response.status_code == 200:
            contributions_data = response.json()
            stats = {
                'total_contributions': contributions_data.get('total_contributions', 0),
                'contributions_by_media_type': contributions_data.get('contributions_by_media_type', {'text': 0, 'audio': 0, 'video': 0, 'image': 0, 'document': 0})
            }
            # Combine all contribution types into one list for recent records
            user_records = []
            user_records.extend(contributions_data.get('text_contributions', [])[:5])
            user_records.extend(contributions_data.get('audio_contributions', [])[:5])
            user_records.extend(contributions_data.get('video_contributions', [])[:5])
            user_records.extend(contributions_data.get('image_contributions', [])[:5])
            user_records.extend(contributions_data.get('document_contributions', [])[:5])
            # Sort by timestamp
            user_records.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
            user_records = user_records[:10]  # Show latest 10 records
    except:
        pass
    
    return render_template('dashboard.html', user=current_user, records=user_records, stats=stats)

# Enhanced content route with media type support
@app.route('/content/<media_type>')
@app.route('/content')
@login_required  
def content(media_type='text'):
    # Get categories from API
    categories = []
    try:
        response = api_request('/categories/', token=current_user.access_token)
        if response and response.status_code == 200:
            categories = response.json()
    except:
        pass
    
    return render_template('content.html', categories=categories, selected_media_type=media_type)

@app.route('/submit-content', methods=['POST'])
def submit_content():
    """
    Submit new content to the backend:
    - Validates request fields
    - Uploads text content as a chunk
    - Finalizes the record upload
    """

    # --- Language Mapping ---
    language_mapping = {
        'english': 'english', 'English': 'english',
        'hindi': 'hindi', 'Hindi': 'hindi',
        'telugu': 'telugu', 'Telugu': 'telugu',
        'tamil': 'tamil', 'Tamil': 'tamil',
        'bengali': 'bengali', 'Bengali': 'bengali',
        'marathi': 'marathi', 'Marathi': 'marathi',
        'gujarati': 'gujarati', 'Gujarati': 'gujarati',
        'kannada': 'kannada', 'Kannada': 'kannada',
        'malayalam': 'malayalam', 'Malayalam': 'malayalam',
        'punjabi': 'punjabi', 'Punjabi': 'punjabi',
        'odia': 'odia', 'Odia': 'odia',
        'urdu': 'urdu', 'Urdu': 'urdu',
        'assamese': 'assamese', 'Assamese': 'assamese',
        'other': 'telugu', 'Other': 'telugu',
        'NA': 'telugu'
    }

    # --- Release Rights Mapping ---
    release_rights_mapping = {
        'creator': 'creator',
        'family_or_friend': 'permission',
        'family': 'permission',
        'permission': 'permission',
        'downloaded': 'unknown',
        'unknown': 'unknown',
        'This work is created by me and anyone is free to use it.': 'creator',
        'This work is created by my family/friends and I took permission to upload their work.': 'permission',
        'I downloaded this from the internet and/or I don\'t know if it is free to share.': 'unknown'
    }

    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({'success': False, 'message': 'Invalid JSON body'}), 400

    # --- Step 1: Validation ---
    title = data.get('title', '').strip()
    if not title:
        return jsonify({'success': False, 'message': 'Title is required'}), 400

    # Pick content from content/description
    content_text = data.get('content') or data.get('description') or ''
    if not content_text or len(content_text.strip()) < 10:
        return jsonify({'success': False, 'message': 'Content must be at least 10 characters long'}), 400

    category_id = data.get('category_id')
    if not category_id:
        return jsonify({'success': False, 'message': 'Category is required'}), 400

    language = data.get('language', '').strip()
    if not language:
        return jsonify({'success': False, 'message': 'Language is required'}), 400
    if language.lower() not in language_mapping:
        return jsonify({'success': False, 'message': f'Language "{language}" is not supported'}), 400

    release_rights = data.get('release_rights', '').strip()
    if not release_rights:
        return jsonify({'success': False, 'message': 'Release rights selection is required'}), 400
    if release_rights not in release_rights_mapping:
        return jsonify({'success': False, 'message': f'Release rights "{release_rights}" is not supported'}), 400

    # --- Step 2: Prepare upload ---
    upload_uuid = str(uuid.uuid4())
    clean_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
    filename = f"{clean_title[:50]}.txt"

    # Check authentication
    if not current_user or not current_user.access_token:
        return jsonify({'success': False, 'message': 'Authentication required'}), 401

    # Upload chunk (only 1 chunk for text)
    chunk_data = {
        'filename': filename,
        'chunk_index': 0,
        'total_chunks': 1,
        'upload_uuid': upload_uuid
    }
    files = {'chunk': (filename, content_text.encode('utf-8'), 'text/plain')}

    chunk_response = api_request('/records/upload/chunk', 'POST', chunk_data,
                                 token=current_user.access_token, files=files)

    if not chunk_response or chunk_response.status_code != 200:
        return jsonify({'success': False, 'message': 'Failed to upload content chunk'}), 400

    # --- Step 3: Finalize upload ---
    record_data = {
        'title': title,
        'description': content_text,
        'media_type': data.get('media_type', 'text'),
        'language': language_mapping[language.lower()],
        'user_id': current_user.id,
        'category_id': category_id,
        'release_rights': release_rights_mapping[release_rights],
        'upload_uuid': upload_uuid,
        'filename': filename,
        'total_chunks': 1,
        'use_uid_filename': False
    }

    # Optional location
    try:
        if data.get('latitude') and data.get('longitude'):
            record_data['latitude'] = float(data['latitude'])
            record_data['longitude'] = float(data['longitude'])
    except (ValueError, TypeError):
        pass  # skip invalid location

    response = api_request('/records/upload', 'POST', record_data,
                           token=current_user.access_token, form_data=True)

    if response and response.status_code == 201:
        return jsonify({'success': True, 'message': 'Content submitted successfully!'}), 201
    elif response and response.status_code == 403:
        return jsonify({'success': False, 'message': 'Authentication expired. Please log in again.'}), 401
    else:
        error_msg = 'Failed to submit content.'
        try:
            if response is not None:
                error_data = response.json()
                if 'detail' in error_data:
                    if isinstance(error_data['detail'], list):
                        error_msg = f"Validation error: {error_data['detail'][0].get('msg', 'Invalid data')}"
                    elif isinstance(error_data['detail'], str):
                        error_msg = error_data['detail']
                elif 'message' in error_data:
                    error_msg = error_data['message']
        except:
            pass
        return jsonify({'success': False, 'message': error_msg}), 400


@app.route('/my-records')
@login_required
def my_records():
    # Get user's contributions from API using the correct endpoint
    records = []
    stats = {'total_contributions': 0, 'contributions_by_media_type': {'text': 0, 'audio': 0, 'video': 0, 'image': 0, 'document': 0}}
    try:
        response = api_request(f'/users/{current_user.id}/contributions', token=current_user.access_token)
        if response and response.status_code == 200:
            contributions_data = response.json()
            stats = {
                'total_contributions': contributions_data.get('total_contributions', 0),
                'contributions_by_media_type': contributions_data.get('contributions_by_media_type', {'text': 0, 'audio': 0, 'video': 0, 'image': 0, 'document': 0})
            }
            # Combine all contribution types into one list
            records = []
            records.extend(contributions_data.get('text_contributions', []))
            records.extend(contributions_data.get('audio_contributions', []))
            records.extend(contributions_data.get('video_contributions', []))
            records.extend(contributions_data.get('image_contributions', []))
            records.extend(contributions_data.get('document_contributions', []))
    except:
        pass
    
    return render_template('my_records.html', records=records, stats=stats)


# Continue with remaining routes from the original code
@app.route('/landmarks')
@login_required
def landmarks():
    return render_template('landmarks.html')

@app.route('/recipes')
@login_required  
def recipes():
    return render_template('recipes.html')

@app.route('/stories')
@login_required
def stories():
    return render_template('stories.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
    }, token=current_user.access_token)
    
    if response and response.status_code == 200:
        return jsonify({'success': True, 'message': 'Password changed successfully'})
    else:
        return jsonify({'success': False, 'message': 'Failed to change password'}), 400

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))

# Add missing routes that are referenced in templates
@app.route('/stories')
@login_required
def stories():
    return redirect(url_for('content', media_type='text'))

@app.route('/recipes')
@login_required
def recipes():
    return redirect(url_for('content', media_type='text'))

@app.route('/landmarks')
@login_required
def landmarks():
    return redirect(url_for('content', media_type='text'))

# Remove the old content route definition that conflicts

# Route for media-specific content submission pages
@app.route('/submit/<media_type>')
@login_required
def submit_media(media_type):
    if media_type not in ['text', 'audio', 'video', 'image', 'document']:
        return redirect(url_for('content'))
    
    # Get categories from API
    categories = []
    try:
        response = api_request('/categories/', token=current_user.access_token)
        if response and response.status_code == 200:
            categories = response.json()
    except:
        pass
    
    return render_template(f'submit_{media_type}.html', categories=categories, media_type=media_type)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)