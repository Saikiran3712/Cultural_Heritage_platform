# app.py - Main Streamlit Application for Cultural Heritage Platform

import streamlit as st
import os
import sys
import requests
from typing import Optional, Dict, List, Any
import json
from datetime import datetime
import uuid

# Load environment variables if .env file exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not available, continue without it

# Configuration with environment variable support
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.corpus.swecha.org/api/v1")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SWECHA_API_KEY = os.getenv("SWECHA_API_KEY")

# Translation dictionaries
TRANSLATIONS = {
    'english': {
        'app_title': 'Indian Cultural Heritage Platform',
        'welcome_back': 'Welcome Back!',
        'login': 'Login',
        'signup': 'Sign Up',
        'otp_login': 'OTP Login',
        'phone_number': 'Phone Number',
        'password': 'Password',
        'full_name': 'Full Name',
        'email': 'Email',
        'create_account': 'Create Account',
        'home': 'Home',
        'dashboard': 'Dashboard',
        'submit_content': 'Submit Content',
        'my_records': 'My Records',
        'profile': 'Profile',
        'logout': 'Logout',
        'welcome_message': 'Welcome to the Indian Cultural Heritage Platform!',
        'about_mission': 'About Our Mission',
        'what_we_collect': 'What We Collect',
        'how_contribute': 'How You Can Contribute',
        'platform_statistics': 'Platform Statistics',
        'content_categories': 'Content Categories',
        'languages_supported': 'Languages Supported',
        'your_contributions': 'Your Contributions',
        'submit_cultural_content': 'Submit Cultural Content',
        'my_contributions': 'My Contributions',
        'user_profile': 'User Profile',
        'change_password': 'Change Password'
    },
    'hindi': {
        'app_title': 'भारतीय सांस्कृतिक विरासत मंच',
        'welcome_back': 'वापसी पर स्वागत!',
        'login': 'लॉगिन',
        'signup': 'साइन अप',
        'otp_login': 'ओटीपी लॉगिन',
        'phone_number': 'फोन नंबर',
        'password': 'पासवर्ड',
        'full_name': 'पूरा नाम',
        'email': 'ईमेल',
        'create_account': 'खाता बनाएं',
        'home': 'होम',
        'dashboard': 'डैशबोर्ड',
        'submit_content': 'सामग्री जमा करें',
        'my_records': 'मेरे रिकॉर्ड',
        'profile': 'प्रोफ़ाइल',
        'logout': 'लॉगआउट',
        'welcome_message': 'भारतीय सांस्कृतिक विरासत मंच में आपका स्वागत है!',
        'about_mission': 'हमारे मिशन के बारे में',
        'what_we_collect': 'हम क्या संग्रह करते हैं',
        'how_contribute': 'आप कैसे योगदान दे सकते हैं',
        'platform_statistics': 'प्लेटफॉर्म आंकड़े',
        'content_categories': 'सामग्री श्रेणियां',
        'languages_supported': 'समर्थित भाषाएं',
        'your_contributions': 'आपके योगदान',
        'submit_cultural_content': 'सांस्कृतिक सामग्री जमा करें',
        'my_contributions': 'मेरे योगदान',
        'user_profile': 'उपयोगकर्ता प्रोफ़ाइल',
        'change_password': 'पासवर्ड बदलें'
    },
    'tamil': {
        'app_title': 'இந்திய கலாச்சார பாரம்பரிய தளம்',
        'welcome_back': 'வரவேற்கிறோம்!',
        'login': 'உள்நுழை',
        'signup': 'பதிவு செய்க',
        'otp_login': 'OTP உள்நுழைவு',
        'phone_number': 'தொலைபேசி எண்',
        'password': 'கடவுச்சொல்',
        'full_name': 'முழு பெயர்',
        'email': 'மின்னஞ்சல்',
        'create_account': 'கணக்கு உருவாக்க',
        'home': 'முகப்பு',
        'dashboard': 'கட்டுப்பாட்டு பலகை',
        'submit_content': 'உள்ளடக்கத்தை சமர்ப்பிக்க',
        'my_records': 'எனது பதிவுகள்',
        'profile': 'சுயவிவரம்',
        'logout': 'வெளியேறு',
        'welcome_message': 'இந்திய கலாச்சார பாரம்பரிய தளத்திற்கு வரவேற்கிறோம்!',
        'about_mission': 'எங்கள் பணி பற்றி',
        'what_we_collect': 'நாம் என்ன சேகரிக்கிறோம்',
        'how_contribute': 'நீங்கள் எப்படி பங்களிக்கலாம்',
        'platform_statistics': 'தள புள்ளிவிவரங்கள்',
        'content_categories': 'உள்ளடக்க வகைகள்',
        'languages_supported': 'ஆதரிக்கப்படும் மொழிகள்',
        'your_contributions': 'உங்கள் பங்களிப்புகள்',
        'submit_cultural_content': 'கலாச்சார உள்ளடக்கத்தை சமர்ப்பிக்க',
        'my_contributions': 'எனது பங்களிப்புகள்',
        'user_profile': 'பயனர் சுயவிவரம்',
        'change_password': 'கடவுச்சொல்லை மாற்று'
    },
    'bengali': {
        'app_title': 'ভারতীয় সাংস্কৃতিক ঐতিহ্য প্ল্যাটফর্ম',
        'welcome_back': 'স্বাগতম!',
        'login': 'লগইন',
        'signup': 'সাইন আপ',
        'otp_login': 'OTP লগইন',
        'phone_number': 'ফোন নম্বর',
        'password': 'পাসওয়ার্ড',
        'full_name': 'পূর্ণ নাম',
        'email': 'ইমেইল',
        'create_account': 'অ্যাকাউন্ট তৈরি করুন',
        'home': 'হোম',
        'dashboard': 'ড্যাশবোর্ড',
        'submit_content': 'বিষয়বস্তু জমা দিন',
        'my_records': 'আমার রেকর্ড',
        'profile': 'প্রোফাইল',
        'logout': 'লগআউট',
        'welcome_message': 'ভারতীয় সাংস্কৃতিক ঐতিহ্য প্ল্যাটফর্মে স্বাগতম!',
        'about_mission': 'আমাদের মিশন সম্পর্কে',
        'what_we_collect': 'আমরা কি সংগ্রহ করি',
        'how_contribute': 'আপনি কিভাবে অবদান রাখতে পারেন',
        'platform_statistics': 'প্ল্যাটফর্ম পরিসংখ্যান',
        'content_categories': 'বিষয়বস্তুর বিভাগ',
        'languages_supported': 'সমর্থিত ভাষা',
        'your_contributions': 'আপনার অবদান',
        'submit_cultural_content': 'সাংস্কৃতিক বিষয়বস্তু জমা দিন',
        'my_contributions': 'আমার অবদান',
        'user_profile': 'ব্যবহারকারী প্রোফাইল',
        'change_password': 'পাসওয়ার্ড পরিবর্তন করুন'
    },
    'telugu': {
        'app_title': 'భారతీయ సాంస్కృతిక వారసత్వ వేదిక',
        'welcome_back': 'తిరిగి స్వాగతం!',
        'login': 'లాగిన్',
        'signup': 'సైన్ అప్',
        'otp_login': 'OTP లాగిన్',
        'phone_number': 'ఫోన్ నంబర్',
        'password': 'పాస్‌వర్డ్',
        'full_name': 'పూర్తి పేరు',
        'email': 'ఇమెయిల్',
        'create_account': 'ఖాతాను సృష్టించండి',
        'home': 'హోమ్',
        'dashboard': 'డాష్‌బోర్డ్',
        'submit_content': 'కంటెంట్ సమర్పించండి',
        'my_records': 'నా రికార్డులు',
        'profile': 'ప్రొఫైల్',
        'logout': 'లాగౌట్',
        'welcome_message': 'భారతీయ సాంస్కృతిక వారసత్వ వేదికకు స్వాగతం!',
        'about_mission': 'మా మిషన్ గురించి',
        'what_we_collect': 'మేము ఏమి సేకరిస్తాము',
        'how_contribute': 'మీరు ఎలా సహకరించవచ్చు',
        'platform_statistics': 'వేదిక గణాంకాలు',
        'content_categories': 'కంటెంట్ వర్గాలు',
        'languages_supported': 'మద్దతు ఉన్న భాషలు',
        'your_contributions': 'మీ సహకారాలు',
        'submit_cultural_content': 'సాంస్కృతిక కంటెంట్ సమర్పించండి',
        'my_contributions': 'నా సహకారాలు',
        'user_profile': 'వినియోగదారు ప్రొఫైల్',
        'change_password': 'పాస్‌వర్డ్ మార్చండి'
    }
}

def get_text(key: str, lang: str | None = None) -> str:
    """Get translated text for a given key"""
    if lang is None:
        lang = st.session_state.get('interface_language', 'english')
        if lang is None:
            lang = 'english'
    
    # Fallback to English if translation not found  
    translations_for_lang = TRANSLATIONS.get(lang, {})
    return translations_for_lang.get(key, TRANSLATIONS['english'].get(key, key))

# Initialize session state
def init_session_state():
    """Initialize all session state variables"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user_data" not in st.session_state:
        st.session_state.user_data = None
    if "access_token" not in st.session_state:
        st.session_state.access_token = None
    if "signup_step" not in st.session_state:
        st.session_state.signup_step = 1
    if "signup_phone_number" not in st.session_state:
        st.session_state.signup_phone_number = ""
    if "interface_language" not in st.session_state:
        st.session_state.interface_language = "english"

# API Helper Functions
def api_request(endpoint: str, method: str = 'GET', data: Optional[Dict] = None, 
                token: Optional[str] = None, form_data: bool = False, files: Optional[Dict] = None) -> Optional[requests.Response]:
    """Make API requests to the corpus API"""
    url = f"{API_BASE_URL}{endpoint}"
    headers = {}
    
    if token:
        headers['Authorization'] = f'Bearer {token}'
    
    # Don't set Content-Type for multipart uploads (requests will set it automatically)
    if not form_data and not files:
        headers['Content-Type'] = 'application/json'
    
    # Debug logging
    if form_data or files:
        st.info(f"Making {method} request to {url}")
        if data:
            st.info(f"Request data keys: {list(data.keys()) if isinstance(data, dict) else type(data)}")
    
    try:
        if method == 'POST':
            if files:
                # For multipart uploads - longer timeout
                response = requests.post(url, data=data, files=files, headers=headers, timeout=60)
            elif form_data:
                # For form data submissions - longer timeout
                response = requests.post(url, data=data, headers=headers, timeout=30)
            else:
                # For JSON data
                response = requests.post(url, json=data, headers=headers, timeout=10)
        elif method == 'GET':
            response = requests.get(url, headers=headers, params=data, timeout=10)
        else:
            return None
        
        # Debug logging for responses
        if form_data or files:
            st.info(f"Response status: {response.status_code}")
            if response.status_code not in [200, 201]:
                st.error(f"Response content: {response.text[:500]}")
            
        return response
    except requests.exceptions.Timeout as e:
        st.error(f"API request timeout after waiting for response: {str(e)}")
        return None
    except requests.exceptions.ConnectionError as e:
        st.error(f"API connection error - could not reach server: {str(e)}")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed ({type(e).__name__}): {str(e)}")
        return None

# Fallback data for when API is not available
def get_fallback_categories():
    """Return fallback categories when API is not available"""
    return [
        {"id": "550e8400-e29b-41d4-a716-446655440001", "name": "Traditional Stories"},
        {"id": "550e8400-e29b-41d4-a716-446655440002", "name": "Folk Tales"},
        {"id": "550e8400-e29b-41d4-a716-446655440003", "name": "Traditional Recipes"},
        {"id": "550e8400-e29b-41d4-a716-446655440004", "name": "Historical Landmarks"},
        {"id": "550e8400-e29b-41d4-a716-446655440005", "name": "Cultural Practices"},
        {"id": "550e8400-e29b-41d4-a716-446655440006", "name": "Folk Songs"},
        {"id": "550e8400-e29b-41d4-a716-446655440007", "name": "Traditional Games"},
        {"id": "550e8400-e29b-41d4-a716-446655440008", "name": "Festivals"}
    ]

def get_fallback_user_data():
    """Return fallback user data when API is not available"""
    return {
        "id": "demo_user",
        "name": "Demo User",
        "phone": "1234567890",
        "email": "demo@example.com",
        "total_contributions": 0
    }

# Language mappings
language_mapping = {
    'telugu': 'telugu',
    'english': 'english',
    'hindi': 'hindi',
    'tamil': 'tamil',
    'bengali': 'bengali',
    'marathi': 'marathi',
    'gujarati': 'gujarati',
    'kannada': 'kannada',
    'malayalam': 'malayalam',
    'punjabi': 'punjabi',
    'odia': 'odia',
    'urdu': 'urdu',
    'assamese': 'assamese'
}

release_rights_mapping = {
    'I created this content myself': 'creator',
    'I have permission from family/friends who created this': 'family_or_friend',
    'I downloaded this or am unsure of the rights': 'downloaded',
    'Not applicable': 'NA'
}

# Page configuration
try:
    st.set_page_config(
        page_title="Cultural Heritage Platform",
        layout="wide",
        initial_sidebar_state="expanded"
    )
except Exception as e:
    # Handle case where set_page_config is called multiple times
    pass

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        font-size: 2.5rem;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .content-card {
        border: 2px solid #e6f3ff;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .telugu-text {
        font-family: "Noto Sans Telugu", sans-serif;
        font-size: 1.2rem;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 10px;
        color: #155724;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        padding: 10px;
        color: #721c24;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 5px;
        padding: 10px;
        color: #0c5460;
    }
</style>
""", unsafe_allow_html=True)

def main():
    init_session_state()
    
    # Language selector in sidebar
    with st.sidebar:
        st.markdown("### 🌐 Interface Language")
        language_options = {
            'English': 'english',
            'हिंदी': 'hindi', 
            'தமிழ்': 'tamil',
            'বাংলা': 'bengali',
            'తెలుగు': 'telugu'
        }
        
        selected_lang_display = st.selectbox(
            "Select Language",
            options=list(language_options.keys()),
            index=list(language_options.values()).index(st.session_state.interface_language),
            key="language_selector"
        )
        
        new_lang = language_options[selected_lang_display]
        if new_lang != st.session_state.interface_language:
            st.session_state.interface_language = new_lang
            st.rerun()
    
    # Check if token exists and try to re-authenticate
    if st.session_state.access_token and not st.session_state.authenticated:
        user_response = api_request('/auth/me', token=st.session_state.access_token)
        if user_response and user_response.status_code == 200:
            st.session_state.user_data = user_response.json()
            st.session_state.authenticated = True
            st.success("Re-authenticated successfully!")
            st.rerun()
        else:
            st.session_state.access_token = None
            st.session_state.authenticated = False
    
    # Main header with translation
    st.markdown(f'<h1 class="main-header">{get_text("app_title")}</h1>', unsafe_allow_html=True)
    st.markdown('<p class="telugu-text" style="text-align: center;">Preserving India\'s Rich Cultural Diversity - भारतीय सांस्कृतिक विविधता को संरक्षित करना</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Authentication check
    if not st.session_state.authenticated:
        show_auth_pages()
    else:
        show_main_app()

def show_auth_pages():
    """Show authentication pages (login/signup)"""
    auth_tab = st.sidebar.selectbox("Choose Action", [get_text("login"), get_text("signup"), get_text("otp_login"), "Forgot Password"])
    
    if auth_tab == get_text("login"):
        show_login_page()
    elif auth_tab == get_text("signup"):
        show_signup_page()
    elif auth_tab == get_text("otp_login"):
        show_otp_login_page()
    else:
        show_forgot_password_page()

def show_login_page():
    """Show login page"""
    st.header(f"🔐 {get_text('login')} to Your Account")
    
    with st.form("login_form"):
        col1, col2 = st.columns([1, 1])
        
        with col1:
            phone_number = st.text_input(get_text("phone_number"), placeholder="Enter your phone number")
            password = st.text_input(get_text("password"), type="password", placeholder="Enter your password")
        
        with col2:
            st.markdown(f"### {get_text('welcome_back')}")
            st.markdown(f"{get_text('login')} to continue contributing to our cultural heritage collection.")
            st.markdown(f"**New here?** Switch to {get_text('signup')} to create an account.")
            st.markdown(f"**Forgot password?** Use {get_text('otp_login')} instead.")
        
        submitted = st.form_submit_button(get_text("login"), use_container_width=True)
        
    if submitted and phone_number and password:
        with st.spinner("Logging in..."):
            result = api_request('/auth/login', 'POST', {
                'phone': phone_number,
                'password': password
            })
            
            if result and result.status_code == 200:
                token_data = result.json()
                access_token = token_data.get('access_token')
                
                if access_token:
                    st.session_state.access_token = access_token
                    
                    # Get user info
                    user_response = api_request('/auth/me', token=access_token)
                    if user_response and user_response.status_code == 200:
                        st.session_state.user_data = user_response.json()
                        st.session_state.authenticated = True
                        st.success("Login successful! Redirecting...")
                        st.rerun()
                    else:
                        st.error("Failed to get user information")
                else:
                    st.error("Login failed - no access token received")
            else:
                st.error("Invalid phone number or password")

def show_otp_login_page():
    """Show OTP-based login page"""
    st.header("📱 OTP Login")
    
    if "otp_step" not in st.session_state:
        st.session_state.otp_step = 1
    if "otp_phone_number" not in st.session_state:
        st.session_state.otp_phone_number = ""
    
    if st.session_state.otp_step == 1:
        st.subheader("Step 1: Enter Phone Number")
        with st.form("send_otp_form"):
            phone_number = st.text_input("Phone Number", placeholder="Enter your registered phone number")
            submitted_otp_send = st.form_submit_button("Send OTP", use_container_width=True)

            if submitted_otp_send and phone_number:
                with st.spinner("Sending OTP..."):
                    result = api_request('/auth/login/send-otp', 'POST', {
                        'phone_number': phone_number
                    })
                    
                    if result and result.status_code == 200:
                        st.session_state.otp_phone_number = phone_number
                        st.session_state.otp_step = 2
                        st.success("OTP sent successfully! Please check your phone.")
                        st.rerun()
                    else:
                        st.error("Failed to send OTP. Please check your phone number.")
    
    elif st.session_state.otp_step == 2:
        st.subheader("Step 2: Enter OTP")
        with st.form("verify_otp_form"):
            st.text_input("Phone Number", value=st.session_state.otp_phone_number, disabled=True)
            otp_code = st.text_input("OTP Code", placeholder="Enter the 6-digit OTP")
            
            col1, col2 = st.columns(2)
            with col1:
                submitted_otp_verify = st.form_submit_button("Verify OTP & Login", use_container_width=True)
            with col2:
                back_button = st.form_submit_button("← Back", use_container_width=True)

            if back_button:
                st.session_state.otp_step = 1
                st.rerun()

            if submitted_otp_verify and otp_code:
                with st.spinner("Verifying OTP..."):
                    result = api_request('/auth/login/verify-otp', 'POST', {
                        'phone_number': st.session_state.otp_phone_number,
                        'otp_code': otp_code
                    })
                    
                    if result and result.status_code == 200:
                        token_data = result.json()
                        access_token = token_data.get('access_token')
                        
                        if access_token:
                            st.session_state.access_token = access_token
                            
                            # Get user info
                            user_response = api_request('/auth/me', token=access_token)
                            if user_response and user_response.status_code == 200:
                                st.session_state.user_data = user_response.json()
                                st.session_state.authenticated = True
                                st.session_state.otp_step = 1  # Reset for next time
                                st.success("Login successful! Redirecting...")
                                st.rerun()
                            else:
                                st.error("Failed to get user information")
                        else:
                            st.error("Login failed - no access token received")
                    else:
                        st.error("Invalid OTP. Please try again.")

def show_forgot_password_page():
    """Show forgot password page with OTP verification"""
    st.header("🔑 Reset Password")
    
    if "forgot_password_step" not in st.session_state:
        st.session_state.forgot_password_step = 1
    if "forgot_password_phone" not in st.session_state:
        st.session_state.forgot_password_phone = ""
    if "forgot_password_reference_id" not in st.session_state:
        st.session_state.forgot_password_reference_id = ""
    
    if st.session_state.forgot_password_step == 1:
        st.subheader("Step 1: Enter Phone Number")
        with st.form("forgot_password_init_form"):
            phone_number = st.text_input("Phone Number", placeholder="Enter your registered phone number")
            submitted = st.form_submit_button("Send Reset OTP", use_container_width=True)

            if submitted and phone_number:
                with st.spinner("Sending password reset OTP..."):
                    result = api_request('/auth/forgot-password/init', 'POST', {
                        'phone_number': phone_number
                    })
                    
                    if result and result.status_code == 200:
                        response_data = result.json()
                        st.session_state.forgot_password_phone = phone_number
                        st.session_state.forgot_password_reference_id = response_data.get('reference_id', '')
                        st.session_state.forgot_password_step = 2
                        st.success("Password reset OTP sent successfully! Please check your phone.")
                        st.rerun()
                    else:
                        st.error("Failed to send password reset OTP. Please check your phone number.")
    
    elif st.session_state.forgot_password_step == 2:
        st.subheader("Step 2: Reset Password")
        with st.form("forgot_password_confirm_form"):
            st.text_input("Phone Number", value=st.session_state.forgot_password_phone, disabled=True)
            otp_code = st.text_input("OTP Code", placeholder="Enter the 6-digit OTP")
            new_password = st.text_input("New Password", type="password", placeholder="Enter your new password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your new password")
            
            col1, col2 = st.columns(2)
            with col1:
                submitted = st.form_submit_button("Reset Password", use_container_width=True)
            with col2:
                back_button = st.form_submit_button("← Back", use_container_width=True)

            if back_button:
                st.session_state.forgot_password_step = 1
                st.rerun()

            if submitted and otp_code and new_password and confirm_password:
                if new_password != confirm_password:
                    st.error("Passwords don't match. Please try again.")
                elif len(new_password) < 6:
                    st.error("Password must be at least 6 characters long.")
                else:
                    with st.spinner("Resetting password..."):
                        result = api_request('/auth/forgot-password/confirm', 'POST', {
                            'phone_number': st.session_state.forgot_password_phone,
                            'otp_code': otp_code,
                            'new_password': new_password,
                            'confirm_password': confirm_password
                        })
                        
                        if result and result.status_code == 200:
                            st.success("Password reset successfully! You can now login with your new password.")
                            st.balloons()
                            # Reset forgot password state
                            st.session_state.forgot_password_step = 1
                            st.session_state.forgot_password_phone = ""
                            st.session_state.forgot_password_reference_id = ""
                            st.rerun()
                        else:
                            if result:
                                if result.status_code == 400:
                                    st.error("❌ Invalid OTP or password. Please check and try again.")
                                elif result.status_code == 404:
                                    st.error("❌ Phone number not found. Please try sending OTP again.")
                                elif result.status_code == 422:
                                    try:
                                        error_detail = result.json().get('detail', 'Validation error')
                                        st.error(f"❌ {error_detail}")
                                    except:
                                        st.error("❌ Invalid input. Please check all fields and try again.")
                                else:
                                    st.error(f"❌ Server error (Code: {result.status_code}). Please try again later.")
                            else:
                                st.error("❌ Connection failed. Please check your internet and try again.")

def show_signup_page():
    """Show OTP-based signup page"""
    st.header("📝 Create New Account")
    
    if st.session_state.signup_step == 1:
        st.subheader("Step 1: Enter Phone Number")
        with st.form("send_signup_otp_form"):
            phone_number = st.text_input("Phone Number", placeholder="Enter your phone number (e.g., +919876543210)")
            submitted_signup_otp = st.form_submit_button("Send OTP", use_container_width=True)

            if submitted_signup_otp and phone_number:
                with st.spinner("Sending OTP..."):
                    result = api_request('/auth/signup/send-otp', 'POST', {
                        'phone_number': phone_number
                    })
                    
                    if result and result.status_code == 200:
                        st.session_state.signup_phone_number = phone_number
                        st.session_state.signup_step = 2
                        st.success("OTP sent successfully! Please check your phone.")
                        st.rerun()
                    else:
                        st.error("Failed to send OTP. Please check your phone number and try again.")
    
    elif st.session_state.signup_step == 2:
        st.subheader("Step 2: Verify OTP and Complete Registration")
        with st.form("verify_signup_otp_form"):
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.text_input("Phone Number", value=st.session_state.signup_phone_number, disabled=True)
                otp_code = st.text_input("OTP Code", placeholder="Enter the 6-digit OTP")
                name = st.text_input("Full Name", placeholder="Enter your full name")
                email = st.text_input("Email", placeholder="Enter your email address")
                password = st.text_input("Password", type="password", placeholder="Create a strong password (min 8 chars)")
                confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
                has_given_consent = st.checkbox("I agree to the terms and conditions and consent to data collection for cultural preservation purposes")
            
            with col2:
                st.markdown("### Join Our Community!")
                st.markdown("Help preserve India's rich cultural heritage for future generations.")
                st.markdown("**What you can contribute:**")
                st.markdown("- 📖 Traditional stories and folklore")
                st.markdown("- 🍽️ Authentic recipes and cooking methods")
                st.markdown("- 🏛️ Historical landmarks and their stories")
                st.markdown("- 🎵 Folk songs and traditional music")
                st.markdown("- 🎭 Cultural practices and festivals")
            
            col_verify, col_back = st.columns([2, 1])
            with col_verify:
                submitted_verify = st.form_submit_button("Verify OTP & Create Account", use_container_width=True)
            with col_back:
                back_button = st.form_submit_button("← Back", use_container_width=True)

            if back_button:
                st.session_state.signup_step = 1
                st.rerun()

            if submitted_verify:
                if not all([otp_code, name, email, password, confirm_password]):
                    st.error("Please fill in all fields.")
                elif password != confirm_password:
                    st.error("Passwords don't match.")
                elif len(password) < 8:
                    st.error("Password must be at least 8 characters long.")
                elif not has_given_consent:
                    st.error("Please agree to the terms and conditions.")
                else:
                    with st.spinner("Verifying OTP and creating account..."):
                        result = api_request('/auth/signup/verify-otp', 'POST', {
                            'phone_number': st.session_state.signup_phone_number,
                            'otp_code': otp_code,
                            'name': name,
                            'email': email,
                            'password': password,
                            'confirm_password': confirm_password,
                            'has_given_consent': has_given_consent
                        })
                        
                        if result and result.status_code == 200:
                            st.success("Account created successfully! You can now login with your credentials.")
                            st.balloons()
                            st.session_state.signup_step = 1  # Reset for next time
                            st.rerun()
                        else:
                            try:
                                error_data = result.json() if result else {}
                                if 'detail' in error_data:
                                    if isinstance(error_data['detail'], list):
                                        error_msg = error_data['detail'][0].get('msg', 'Registration failed')
                                    else:
                                        error_msg = error_data['detail']
                                else:
                                    error_msg = "OTP verification failed or registration error. Please try again."
                            except:
                                error_msg = "Registration failed. Please try again."
                            
                            st.error(error_msg)

def show_main_app():
    """Show main application after authentication"""
    # Sidebar navigation
    st.sidebar.title("Navigation")
    st.sidebar.markdown(f"**{get_text('welcome_back')}, {st.session_state.user_data.get('name', 'User')}!**")
    
    page = st.sidebar.selectbox(
        "Choose a page",
        [get_text("home"), get_text("dashboard"), get_text("submit_content"), get_text("my_records"), get_text("profile")]
    )
    
    # Logout button
    if st.sidebar.button(get_text("logout"), use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.user_data = None
        st.session_state.access_token = None
        st.rerun()
    
    # Route to appropriate page
    if page == get_text("home"):
        show_home_page()
    elif page == get_text("dashboard"):
        show_dashboard()
    elif page == get_text("submit_content"):
        show_submit_content_page()
    elif page == get_text("my_records"):
        show_my_records_page()
    elif page == get_text("profile"):
        show_profile_page()

def show_home_page():
    """Show the home page with project overview"""
    st.header(get_text("welcome_message"))
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
        ### 🌟 {get_text("about_mission")}
        
        Our platform is dedicated to preserving and documenting India's rich cultural heritage. 
        We collect stories, recipes, landmarks, and traditions from across the diverse regions of our beautiful country.
        
        ### 📚 {get_text("what_we_collect")}
        - **Traditional Stories**: Folk tales, legends, and oral histories
        - **Authentic Recipes**: Regional cuisines and cooking traditions
        - **Historical Landmarks**: Places of cultural and historical significance
        - **Folk Songs**: Traditional music and lyrics
        - **Cultural Practices**: Festivals, ceremonies, and customs
        
        ### 🤝 {get_text("how_contribute")}
        Share your knowledge and memories to help preserve our cultural heritage for future generations. 
        Every contribution, no matter how small, adds to our collective cultural memory.
        """)
    
    with col2:
        st.markdown(f"### 📊 {get_text('platform_statistics')}")
        
        # Get some basic stats
        try:
            categories_response = api_request('/categories/')
            if categories_response and categories_response.status_code == 200:
                categories = categories_response.json()
                st.metric(get_text("content_categories"), len(categories))
            else:
                # Use fallback categories
                fallback_categories = get_fallback_categories()
                st.metric(get_text("content_categories"), f"{len(fallback_categories)}+")
        except:
            fallback_categories = get_fallback_categories()
            st.metric(get_text("content_categories"), f"{len(fallback_categories)}+")
        
        st.metric(get_text("languages_supported"), len(language_mapping))
        st.metric(get_text("your_contributions"), st.session_state.user_data.get('total_contributions', 0))
        
        st.markdown(f"### 🌐 {get_text('languages_supported')}")
        languages = list(language_mapping.keys())[:6]  # Show first 6
        for lang in languages:
            st.markdown(f"• {lang.title()}")
        if len(language_mapping) > 6:
            st.markdown(f"• ... and {len(language_mapping) - 6} more")

def show_dashboard():
    """Show user dashboard with statistics and recent activity"""
    st.header(f"📊 {get_text('dashboard')}")
    
    # Get user contributions
    try:
        user_id = st.session_state.user_data.get('id')
        if user_id:
            contributions_response = api_request(
                f'/users/{user_id}/contributions', 
                token=st.session_state.access_token
            )
            
            if contributions_response and contributions_response.status_code == 200:
                contributions_data = contributions_response.json()
                
                # Display statistics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Contributions", contributions_data.get('total_contributions', 0))
                
                with col2:
                    media_stats = contributions_data.get('contributions_by_media_type', {})
                    st.metric("Text Contributions", media_stats.get('text', 0))
                
                with col3:
                    st.metric("Audio Contributions", media_stats.get('audio', 0))
                
                with col4:
                    st.metric("Video Contributions", media_stats.get('video', 0))
                
                # Show recent contributions
                st.subheader("📋 Your Recent Contributions")
                
                all_contributions = []
                for contrib_type in ['text_contributions', 'audio_contributions', 'video_contributions', 'image_contributions', 'document_contributions']:
                    contributions = contributions_data.get(contrib_type, [])
                    for contrib in contributions[:5]:  # Latest 5 from each type
                        contrib['type'] = contrib_type.replace('_contributions', '')
                        all_contributions.append(contrib)
                
                # Sort by timestamp
                all_contributions.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
                
                if all_contributions:
                    for contrib in all_contributions[:10]:  # Show latest 10
                        with st.expander(f"{contrib.get('title', 'Untitled')} ({contrib.get('type', 'unknown').title()})"):
                            st.write(f"**Description:** {contrib.get('description', 'No description')[:200]}...")
                            st.write(f"**Language:** {contrib.get('language', 'Not specified')}")
                            st.write(f"**Submitted:** {contrib.get('timestamp', 'Unknown')}")
                else:
                    st.info("No contributions yet. Start by submitting some content!")
            else:
                # Show demo dashboard when API is not available
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Contributions", 0)
                
                with col2:
                    st.metric("Text Contributions", 0)
                
                with col3:
                    st.metric("Audio Contributions", 0)
                
                with col4:
                    st.metric("Video Contributions", 0)
                
                st.subheader("📋 Your Recent Contributions")
                st.info("👋 Welcome! Start contributing to see your dashboard with real data.")
    except Exception:
        # Show demo dashboard on any error
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Contributions", 0)
        with col2:
            st.metric("Text Contributions", 0)
        with col3:
            st.metric("Audio Contributions", 0)
        with col4:
            st.metric("Video Contributions", 0)
        
        st.subheader("📋 Your Recent Contributions")
        st.info("👋 Welcome! Start contributing to see your dashboard with real data.")

def show_submit_content_page():
    """Show content submission form with multiple content types"""
    st.header("📝 Submit Cultural Content")
    
    # Content type selection with card-style layout
    st.markdown("### Choose Content Type")
    
    # Content type cards layout
    col1, col2 = st.columns(2)
    
    with col1:
        text_card = st.container()
        with text_card:
            if st.button("📝 **Text Input**\n\nType your content", use_container_width=True, key="text_input"):
                st.session_state.content_type = "text"
        
        video_card = st.container()
        with video_card:
            if st.button("🎥 **Video Content**\n\nRecord or upload video", use_container_width=True, key="video_content"):
                st.session_state.content_type = "video"
        
        document_card = st.container()
        with document_card:
            if st.button("📄 **Document Upload**\n\nUpload document files (PDF, DOCX, etc.)", use_container_width=True, key="document_upload"):
                st.session_state.content_type = "document"
    
    with col2:
        audio_card = st.container()
        with audio_card:
            if st.button("🎤 **Audio Recording**\n\nRecord your voice", use_container_width=True, key="audio_recording"):
                st.session_state.content_type = "audio"
        
        photo_card = st.container()
        with photo_card:
            if st.button("📷 **Photo Capture**\n\nTake or upload photos", use_container_width=True, key="photo_capture"):
                st.session_state.content_type = "image"
    
    # Initialize content type if not set
    if 'content_type' not in st.session_state:
        st.session_state.content_type = "text"
    
    st.markdown("---")
    
    # Show selected content type
    content_type_labels = {
        "text": "📝 Text Input",
        "audio": "🎤 Audio Recording", 
        "video": "🎥 Video Content",
        "image": "📷 Photo Capture",
        "document": "📄 Document Upload"
    }
    
    st.subheader(f"Selected: {content_type_labels[st.session_state.content_type]}")
    
    # Get categories first - try different API endpoints
    categories_response = None
    categories = []
    
    # Try the authenticated endpoint first
    if st.session_state.access_token:
        categories_response = api_request('/categories/', token=st.session_state.access_token)
    
    # If that fails, try without auth
    if not categories_response or categories_response.status_code != 200:
        categories_response = api_request('/categories/')
    
    # Try alternative endpoint
    if not categories_response or categories_response.status_code != 200:
        categories_response = api_request('/category/')
        
    if categories_response and categories_response.status_code == 200:
        categories = categories_response.json()
        if categories:
            st.info(f"✅ Loaded {len(categories)} categories from API")
            # Debug: Show first few categories
            with st.expander("Debug: Available Categories"):
                for cat in categories[:3]:
                    st.text(f"ID: {cat.get('id')}, Name: {cat.get('name')}")
    
    # For now, allow using fallback categories but warn the user
    if not categories:
        st.warning("⚠️ Using demo categories. Some submissions may fail.")
        st.info("The app will work but submissions might not succeed until API connection is restored.")
        categories = get_fallback_categories()
    
    # Show appropriate form based on content type
    with st.form("submit_content_form"):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Basic information
            title = st.text_input("Title *", placeholder="Enter a descriptive title")
            
            # Content input based on type
            content = ""
            uploaded_file = None
            
            if st.session_state.content_type == "text":
                content = st.text_area("Content/Description *", height=200, 
                                     placeholder="Describe your cultural content in detail...")
            
            elif st.session_state.content_type == "audio":
                st.info("🎤 Audio recording functionality")
                uploaded_file = st.file_uploader("Upload Audio File", type=['mp3', 'wav', 'ogg', 'm4a'])
                content = st.text_area("Description *", height=150, 
                                     placeholder="Describe your audio content...")
            
            elif st.session_state.content_type == "video":
                st.info("🎥 Video upload functionality")
                uploaded_file = st.file_uploader("Upload Video File", type=['mp4', 'avi', 'mov', 'mkv'])
                content = st.text_area("Description *", height=150, 
                                     placeholder="Describe your video content...")
            
            elif st.session_state.content_type == "image":
                st.info("📷 Photo upload functionality")
                uploaded_file = st.file_uploader("Upload Image File", type=['jpg', 'jpeg', 'png', 'gif'])
                content = st.text_area("Description *", height=150, 
                                     placeholder="Describe your image content...")
            
            elif st.session_state.content_type == "document":
                st.info("📄 Document upload functionality")
                uploaded_file = st.file_uploader("Upload Document File", type=['pdf', 'docx', 'doc', 'txt'])
                content = st.text_area("Description *", height=150, 
                                     placeholder="Describe your document content...")
            
            # Category selection
            category_options = {cat['name']: cat['id'] for cat in categories}
            selected_category = st.selectbox("Category *", list(category_options.keys()))
            
            language = st.selectbox("Language *", list(language_mapping.keys()))
            release_rights = st.selectbox("Release Rights *", list(release_rights_mapping.keys()))
            
            # Place field instead of latitude/longitude
            place = st.text_input("Place (optional)", placeholder="Enter city, region, or landmark name")
        
        with col2:
            st.markdown("### 📋 Submission Guidelines")
            st.markdown("""
            **Required fields are marked with ***
            
            **Tips for good submissions:**
            - Use clear, descriptive titles
            - Provide detailed descriptions
            - Include cultural context
            - Mention the region/community if relevant
            
            **Content Types:**
            - Stories and folklore
            - Traditional recipes
            - Historical landmarks
            - Cultural practices
            - Folk songs and music
            """)
        
        submitted = st.form_submit_button("Submit Content", use_container_width=True)
        
    if submitted:
        # Validation
        if not title or not content or not selected_category or not language or not release_rights:
            st.error("Please fill in all required fields marked with *")
        elif len(content.strip()) < 10:
            st.error("Content must be at least 10 characters long")
        else:
            with st.spinner("Submitting your content..."):
                # Prepare submission data
                submission_data = {
                    'title': title,
                    'content': content,
                    'category_id': category_options[selected_category],
                    'language': language,
                    'release_rights': release_rights,
                    'media_type': st.session_state.content_type,
                    'place': place if place else None
                }
                
                # Handle file upload or text content
                if uploaded_file and st.session_state.content_type != "text":
                    success, message = submit_file_content(submission_data, uploaded_file, content)
                else:
                    success, message = submit_content_chunk(submission_data, content)
                
                if success:
                    st.success("🎉 Content submitted successfully!")
                    st.balloons()
                    # Clear form by rerunning
                    st.rerun()
                else:
                    st.error(f"Submission failed: {message}")

def submit_content_chunk(data: Dict[str, Any], content_text: str) -> tuple[bool, str]:
    """Handle content submission with chunk upload process"""
    try:
        # Step 1: Upload content chunk
        upload_uuid = str(uuid.uuid4())
        clean_title = "".join(c for c in data['title'] if c.isalnum() or c in (' ', '-', '_')).strip()
        if not clean_title:
            clean_title = "content"
        filename = f"{clean_title[:50]}.txt"
        
        chunk_payload = {
            'filename': filename,
            'chunk_index': 0,
            'total_chunks': 1,
            'upload_uuid': upload_uuid
        }
        
        # Prepare file content
        from io import BytesIO
        content_bytes = content_text.encode('utf-8')
        file_obj = BytesIO(content_bytes)
        files = {'chunk': (filename, file_obj, 'text/plain')}
        
        # Upload chunk
        chunk_response = api_request(
            '/records/upload/chunk',
            method='POST',
            data=chunk_payload,
            token=st.session_state.access_token,
            files=files
        )
        
        if not chunk_response or chunk_response.status_code != 200:
            if chunk_response and chunk_response.status_code == 500:
                try:
                    error_data = chunk_response.json()
                    if error_data.get('detail') == 'Failed to save chunk':
                        return False, 'The server is experiencing issues saving your content. This might be a temporary problem with the external API. Please try again in a few moments.'
                except:
                    pass
            return False, 'Failed to upload content chunk. Please try again.'
        
        # Step 2: Finalize record
        record_data = {
            'title': data['title'],
            'description': content_text,
            'category_id': str(data['category_id']),
            'user_id': str(st.session_state.user_data.get('id')),
            'media_type': data.get('media_type', 'text'),
            'upload_uuid': upload_uuid,
            'filename': filename,
            'total_chunks': 1,
            'release_rights': release_rights_mapping[data['release_rights']],
            'language': language_mapping[data['language']],
            'use_uid_filename': False
        }
        
        # Add place if provided
        if data.get('place'):
            record_data['place'] = str(data['place'])
        
        # Debug logging
        st.info(f"Debug - Sending record data: {record_data}")
        
        # Finalize upload
        response = api_request(
            '/records/upload',
            method='POST',
            data=record_data,
            token=st.session_state.access_token,
            form_data=True
        )
        
        if response and response.status_code == 201:
            return True, 'Content submitted successfully!'
        else:
            # Get detailed error information
            if response:
                try:
                    error_data = response.json()
                    error_msg = f"API Error ({response.status_code}): {error_data.get('detail', response.text)}"
                    st.error(f"Debug - Full response: {response.text}")
                    return False, error_msg
                except:
                    error_msg = f"HTTP Error ({response.status_code}): {response.text[:200]}"
                    st.error(f"Debug - Response status: {response.status_code}, Content: {response.text}")
                    return False, error_msg
            else:
                return False, 'No response received from API server.'
            
    except Exception as e:
        return False, f'An error occurred: {str(e)}'

def submit_file_content(data: Dict[str, Any], uploaded_file, content_text: str) -> tuple[bool, str]:
    """Handle file content submission with chunk upload process"""
    try:
        # Step 1: Upload file chunk
        upload_uuid = str(uuid.uuid4())
        
        # Get file extension and create proper filename
        file_extension = uploaded_file.name.split('.')[-1] if '.' in uploaded_file.name else 'bin'
        clean_title = "".join(c for c in data['title'] if c.isalnum() or c in (' ', '-', '_')).strip()
        if not clean_title:
            clean_title = "content"
        filename = f"{clean_title[:50]}.{file_extension}"
        
        chunk_payload = {
            'filename': filename,
            'chunk_index': 0,
            'total_chunks': 1,
            'upload_uuid': upload_uuid
        }
        
        # Prepare file for upload
        uploaded_file.seek(0)  # Reset file pointer to beginning
        files = {'chunk': (filename, uploaded_file, uploaded_file.type)}
        
        # Upload chunk
        chunk_response = api_request(
            '/records/upload/chunk',
            method='POST',
            data=chunk_payload,
            token=st.session_state.access_token,
            files=files
        )
        
        if not chunk_response or chunk_response.status_code != 200:
            if chunk_response and chunk_response.status_code == 500:
                try:
                    error_data = chunk_response.json()
                    if error_data.get('detail') == 'Failed to save chunk':
                        return False, 'The server is experiencing issues saving your file. This might be a temporary problem with the external API. Please try again in a few moments.'
                except:
                    pass
            return False, 'Failed to upload file chunk. Please try again.'
        
        # Step 2: Finalize record
        record_data = {
            'title': data['title'],
            'description': content_text,
            'category_id': str(data['category_id']),
            'user_id': str(st.session_state.user_data.get('id')),
            'media_type': data.get('media_type', 'text'),
            'upload_uuid': upload_uuid,
            'filename': filename,
            'total_chunks': 1,
            'release_rights': release_rights_mapping[data['release_rights']],
            'language': language_mapping[data['language']],
            'use_uid_filename': False
        }
        
        # Add place if provided
        if data.get('place'):
            record_data['place'] = str(data['place'])
        
        # Debug logging
        st.info(f"Debug - Sending record data: {record_data}")
        
        # Finalize upload
        response = api_request(
            '/records/upload',
            method='POST',
            data=record_data,
            token=st.session_state.access_token,
            form_data=True
        )
        
        if response and response.status_code == 201:
            return True, 'File content submitted successfully!'
        else:
            # Get detailed error information
            if response:
                try:
                    error_data = response.json()
                    error_msg = f"API Error ({response.status_code}): {error_data.get('detail', response.text)}"
                    st.error(f"Debug - Full response: {response.text}")
                    return False, error_msg
                except:
                    error_msg = f"HTTP Error ({response.status_code}): {response.text[:200]}"
                    st.error(f"Debug - Response status: {response.status_code}, Content: {response.text}")
                    return False, error_msg
            else:
                return False, 'No response received from API server.'
            
    except Exception as e:
        return False, f'An error occurred while uploading file: {str(e)}'

def show_my_records_page():
    """Show user's submitted records"""
    st.header(f"📚 {get_text('my_contributions')}")
    
    try:
        user_id = st.session_state.user_data.get('id')
        if not user_id:
            st.error("❌ User ID not found. Please try logging in again.")
            return
            
        # Try to fetch contributions using the most likely endpoint
        with st.spinner("Loading your contributions..."):
            contributions_response = api_request(
                f'/users/{user_id}/contributions', 
                token=st.session_state.access_token
            )
        
        if contributions_response and contributions_response.status_code == 200:
            contributions_data = contributions_response.json()
            
            # Show total contributions count
            total_contributions = contributions_data.get('total_contributions', 0)
            st.metric("📊 Total Contributions", total_contributions)
            
            if total_contributions > 0:
                # Create tabs for different media types
                tab1, tab2, tab3, tab4, tab5 = st.tabs(["📝 Text", "🎵 Audio", "📹 Video", "🖼️ Images", "📄 Documents"])
                
                with tab1:
                    text_contribs = contributions_data.get('text_contributions', [])
                    if text_contribs:
                        st.write(f"**Text Contributions:** {len(text_contribs)}")
                        for idx, contrib in enumerate(text_contribs):
                            with st.expander(f"📝 {contrib.get('title', f'Text {idx+1}')}"):
                                col1, col2 = st.columns([2, 1])
                                with col1:
                                    st.write(f"**Description:** {contrib.get('description', 'No description')}")
                                    st.write(f"**Language:** {contrib.get('language', 'Not specified')}")
                                with col2:
                                    st.write(f"**Date:** {contrib.get('timestamp', 'Not available')[:10] if contrib.get('timestamp') else 'Not available'}")
                                    st.write(f"**Status:** {'✅ Reviewed' if contrib.get('reviewed') else '⏳ Pending'}")
                    else:
                        st.info("No text contributions found.")
                
                with tab2:
                    audio_contribs = contributions_data.get('audio_contributions', [])
                    if audio_contribs:
                        st.write(f"**Audio Contributions:** {len(audio_contribs)}")
                        for idx, contrib in enumerate(audio_contribs):
                            with st.expander(f"🎵 {contrib.get('title', f'Audio {idx+1}')}"):
                                col1, col2 = st.columns([2, 1])
                                with col1:
                                    st.write(f"**Description:** {contrib.get('description', 'No description')}")
                                    st.write(f"**Language:** {contrib.get('language', 'Not specified')}")
                                    if contrib.get('duration'):
                                        st.write(f"**Duration:** {contrib.get('duration')} seconds")
                                with col2:
                                    st.write(f"**Date:** {contrib.get('timestamp', 'Not available')[:10] if contrib.get('timestamp') else 'Not available'}")
                                    st.write(f"**Status:** {'✅ Reviewed' if contrib.get('reviewed') else '⏳ Pending'}")
                    else:
                        st.info("No audio contributions found.")
                
                with tab3:
                    video_contribs = contributions_data.get('video_contributions', [])
                    if video_contribs:
                        st.write(f"**Video Contributions:** {len(video_contribs)}")
                        for idx, contrib in enumerate(video_contribs):
                            with st.expander(f"📹 {contrib.get('title', f'Video {idx+1}')}"):
                                col1, col2 = st.columns([2, 1])
                                with col1:
                                    st.write(f"**Description:** {contrib.get('description', 'No description')}")
                                    st.write(f"**Language:** {contrib.get('language', 'Not specified')}")
                                    if contrib.get('duration'):
                                        st.write(f"**Duration:** {contrib.get('duration')} seconds")
                                with col2:
                                    st.write(f"**Date:** {contrib.get('timestamp', 'Not available')[:10] if contrib.get('timestamp') else 'Not available'}")
                                    st.write(f"**Status:** {'✅ Reviewed' if contrib.get('reviewed') else '⏳ Pending'}")
                    else:
                        st.info("No video contributions found.")
                        
                with tab4:
                    image_contribs = contributions_data.get('image_contributions', [])
                    if image_contribs:
                        st.write(f"**Image Contributions:** {len(image_contribs)}")
                        for idx, contrib in enumerate(image_contribs):
                            with st.expander(f"🖼️ {contrib.get('title', f'Image {idx+1}')}"):
                                col1, col2 = st.columns([2, 1])
                                with col1:
                                    st.write(f"**Description:** {contrib.get('description', 'No description')}")
                                    st.write(f"**Language:** {contrib.get('language', 'Not specified')}")
                                with col2:
                                    st.write(f"**Date:** {contrib.get('timestamp', 'Not available')[:10] if contrib.get('timestamp') else 'Not available'}")
                                    st.write(f"**Status:** {'✅ Reviewed' if contrib.get('reviewed') else '⏳ Pending'}")
                    else:
                        st.info("No image contributions found.")
                        
                with tab5:
                    doc_contribs = contributions_data.get('document_contributions', [])
                    if doc_contribs:
                        st.write(f"**Document Contributions:** {len(doc_contribs)}")
                        for idx, contrib in enumerate(doc_contribs):
                            with st.expander(f"📄 {contrib.get('title', f'Document {idx+1}')}"):
                                col1, col2 = st.columns([2, 1])
                                with col1:
                                    st.write(f"**Description:** {contrib.get('description', 'No description')}")
                                    st.write(f"**Language:** {contrib.get('language', 'Not specified')}")
                                with col2:
                                    st.write(f"**Date:** {contrib.get('timestamp', 'Not available')[:10] if contrib.get('timestamp') else 'Not available'}")
                                    st.write(f"**Status:** {'✅ Reviewed' if contrib.get('reviewed') else '⏳ Pending'}")
                    else:
                        st.info("No document contributions found.")
            
            else:
                st.info("🎯 You haven't submitted any content yet!")
                st.markdown("### Start Contributing")
                st.markdown("• Go to **Submit Content** to add your first contribution")
                st.markdown("• Share traditional stories, recipes, games, or cultural practices") 
                st.markdown("• Help preserve India's rich cultural heritage")
                
        elif contributions_response and contributions_response.status_code == 401:
            st.error("🔒 Authentication failed. Please log in again.")
        elif contributions_response and contributions_response.status_code == 404:
            st.warning("⚠️ Contributions endpoint not found. Using fallback display.")
            # Show empty state but don't show error
            st.info("🎯 You haven't submitted any content yet!")
            st.markdown("### Start Contributing")
            st.markdown("• Go to **Submit Content** to add your first contribution")
            st.markdown("• Share traditional stories, recipes, games, or cultural practices") 
            st.markdown("• Help preserve India's rich cultural heritage")
        else:
            status_code = contributions_response.status_code if contributions_response else "No response"
            st.error(f"❌ Could not load your contributions (Status: {status_code})")
            st.info("💡 This might be because:")
            st.info("• Your submissions are still being processed")
            st.info("• There's a temporary server issue")
            st.info("• The API service is being updated")
            if contributions_response:
                try:
                    error_detail = contributions_response.text[:200]
                    if error_detail:
                        st.text_area("Debug Info:", error_detail, height=100)
                except:
                    pass
            
            if st.button("🔄 Retry"):
                st.rerun()
                
    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")
        st.info("Please try refreshing the page or contact support if the problem persists.")

def show_profile_page():
    """Show user profile page"""
    st.header(f"👤 {get_text('user_profile')}")
    
    if st.session_state.user_data:
        user = st.session_state.user_data
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Profile Information")
            st.write(f"**Name:** {user.get('name', 'Not specified')}")
            st.write(f"**Phone:** {user.get('phone', 'Not specified')}")
            st.write(f"**Email:** {user.get('email', 'Not specified')}")
            st.write(f"**Member Since:** {user.get('created_at', 'Unknown')}")
        
        with col2:
            st.subheader("Contribution Summary")
            
            # Get detailed stats
            try:
                user_id = user.get('id')
                if user_id:
                    contributions_response = api_request(
                        f'/users/{user_id}/contributions', 
                        token=st.session_state.access_token
                    )
                    
                    if contributions_response and contributions_response.status_code == 200:
                        contributions_data = contributions_response.json()
                        media_stats = contributions_data.get('contributions_by_media_type', {})
                        
                        st.metric("Total Contributions", contributions_data.get('total_contributions', 0))
                        st.write(f"**Text:** {media_stats.get('text', 0)}")
                        st.write(f"**Audio:** {media_stats.get('audio', 0)}")
                        st.write(f"**Video:** {media_stats.get('video', 0)}")
                        st.write(f"**Images:** {media_stats.get('image', 0)}")
                        st.write(f"**Documents:** {media_stats.get('document', 0)}")
            except:
                st.write("Unable to load contribution statistics")
        
        st.markdown("---")
        st.subheader("Account Settings")
        
        # Password change form
        with st.expander("Change Password"):
            with st.form("change_password_form"):
                current_password = st.text_input("Current Password", type="password")
                new_password = st.text_input("New Password", type="password")
                confirm_new_password = st.text_input("Confirm New Password", type="password")
                
                change_password_btn = st.form_submit_button("Change Password")
                
                if change_password_btn:
                    if not all([current_password, new_password, confirm_new_password]):
                        st.error("Please fill in all password fields")
                    elif new_password != confirm_new_password:
                        st.error("New passwords don't match")
                    elif len(new_password) < 8:
                        st.error("New password must be at least 8 characters long")
                    else:
                        with st.spinner("Changing password..."):
                            result = api_request('/auth/change-password', 'POST', {
                                'current_password': current_password,
                                'new_password': new_password
                            }, token=st.session_state.access_token)
                            
                            if result and result.status_code == 200:
                                st.success("Password changed successfully!")
                            else:
                                try:
                                    error_data = result.json() if result else {}
                                    error_msg = error_data.get('detail', 'Failed to change password. Please check your current password.')
                                except:
                                    error_msg = "Failed to change password. Please try again."
                                st.error(error_msg)

if __name__ == "__main__":
    main()