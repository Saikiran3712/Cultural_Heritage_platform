"""
Streamlit Application for మన ఆటలు (Mana Aatalu) - Traditional Games Platform
Rewritten version with improved structure, error handling, and code organization.
"""

import streamlit as st
import os
from typing import Optional, Dict, List, Any
import pandas as pd
from datetime import datetime
import uuid
import json
from dataclasses import dataclass
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration and Constants
@dataclass
class Config:
    """Application configuration"""
    page_title: str = "మన ఆటలు - Our Traditional Games"
    layout: str = "wide"
    initial_sidebar_state: str = "expanded"
    min_password_length: int = 6
    min_description_length: int = 32
    max_recent_contributions: int = 10

config = Config()

class SessionStateManager:
    """Manage Streamlit session state with type safety"""
    
    @staticmethod
    def initialize():
        """Initialize all session state variables"""
        defaults = {
            "authenticated": False,
            "user_data": None,
            "access_token": None,
            "current_page": "Home",
            "signup_step": 1,
            "signup_phone_number": "",
            "signup_name": "",
            "signup_email": "",
            "signup_password": "",
            "signup_consent": False,
        }
        
        for key, default_value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = default_value
    
    @staticmethod
    def reset_auth():
        """Reset authentication-related session state"""
        st.session_state.authenticated = False
        st.session_state.user_data = None
        st.session_state.access_token = None
    
    @staticmethod
    def reset_signup():
        """Reset signup-related session state"""
        st.session_state.signup_step = 1
        st.session_state.signup_phone_number = ""
        st.session_state.signup_name = ""
        st.session_state.signup_email = ""
        st.session_state.signup_password = ""
        st.session_state.signup_consent = False

class APIClientWrapper:
    """Wrapper for API client with error handling and caching"""
    
    def __init__(self):
        # In a real implementation, you would initialize your API client here
        # For now, this is a placeholder structure
        self.client = None
        self.base_url = os.getenv("API_BASE_URL", "https://api.corpus.swecha.org/api/v1")
    
    def set_auth_token(self, token: str) -> None:
        """Set authentication token"""
        if self.client:
            # Set token on your actual API client
            pass
    
    def login_for_access_token(self, phone: str, password: str) -> Optional[Dict[str, Any]]:
        """Login and get access token"""
        # Implement actual login logic here
        return {"access_token": "dummy_token"}  # Placeholder
    
    def read_users_me(self) -> Optional[Dict[str, Any]]:
        """Get current user profile"""
        # Implement actual user profile fetching here
        return {"id": "1", "full_name": "User", "phone": "1234567890"}  # Placeholder
    
    def get_categories(self) -> Optional[List[Dict[str, Any]]]:
        """Get available categories"""
        # Implement actual categories fetching here
        return [{"id": 1, "name": "Traditional Games"}, {"id": 2, "name": "Folk Games"}]  # Placeholder
    
    def send_signup_otp(self, phone: str) -> bool:
        """Send OTP for signup"""
        # Implement actual OTP sending logic here
        return True  # Placeholder
    
    def verify_signup_otp(self, phone: str, otp: str, name: str, email: str, password: str, consent: bool) -> bool:
        """Verify OTP and create account"""
        # Implement actual OTP verification and account creation here
        return True  # Placeholder
    
    def resend_signup_otp(self, phone: str) -> bool:
        """Resend OTP"""
        # Implement actual OTP resending logic here
        return True  # Placeholder
    
    def get_user_contributions_by_media(self, user_id: str, media_type: str) -> Optional[Dict[str, Any]]:
        """Get user contributions by media type"""
        # Implement actual contributions fetching here
        return {"contributions": []}  # Placeholder

# Initialize API client
@st.cache_resource
def get_api_client():
    """Get cached API client instance"""
    return APIClientWrapper()

class StyleManager:
    """Manage custom CSS styles"""
    
    @staticmethod
    def load_styles():
        """Load custom CSS styles"""
        st.markdown("""
        <style>
            /* Import Telugu font */
            @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Telugu:wght@400;700&display=swap');
            
            .main-header {
                text-align: center;
                color: #1f77b4;
                font-size: 2.5rem;
                margin-bottom: 2rem;
                font-weight: bold;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
            }
            
            .game-card {
                border: 2px solid #e6f3ff;
                border-radius: 12px;
                padding: 1.5rem;
                margin: 1rem 0;
                background: linear-gradient(135deg, #f8f9ff 0%, #e6f3ff 100%);
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                transition: transform 0.2s ease;
            }
            
            .game-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 12px rgba(0,0,0,0.15);
            }
            
            .telugu-text {
                font-family: "Noto Sans Telugu", sans-serif;
                font-size: 1.2rem;
                line-height: 1.6;
            }
            
            .success-box {
                background-color: #d4edda;
                border: 1px solid #c3e6cb;
                border-radius: 8px;
                padding: 12px;
                color: #155724;
                margin: 10px 0;
            }
            
            .error-box {
                background-color: #f8d7da;
                border: 1px solid #f5c6cb;
                border-radius: 8px;
                padding: 12px;
                color: #721c24;
                margin: 10px 0;
            }
            
            .metric-container {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 12px;
                padding: 20px;
                color: white;
                text-align: center;
                margin: 10px 0;
            }
            
            .sidebar-logo {
                text-align: center;
                padding: 20px 0;
                border-bottom: 1px solid #e0e0e0;
                margin-bottom: 20px;
            }
        </style>
        """, unsafe_allow_html=True)

class AuthenticationHandler:
    """Handle authentication-related operations"""
    
    def __init__(self, api_client: APIClientWrapper):
        self.api_client = api_client
    
    def show_login_page(self):
        """Display login page"""
        st.header("🔐 Login to Your Account")
        
        with st.form("login_form"):
            col1, col2 = st.columns([1, 1])
            
            with col1:
                phone_number = st.text_input(
                    "Phone Number", 
                    placeholder="Enter your phone number",
                    help="Enter your registered phone number"
                )
                password = st.text_input(
                    "Password", 
                    type="password", 
                    placeholder="Enter your password",
                    help="Enter your account password"
                )
            
            with col2:
                st.markdown("### Welcome Back! 👋")
                st.markdown("Login to continue contributing to our traditional games collection.")
                st.info("**New here?** Switch to Sign Up to create an account.")
            
            submitted = st.form_submit_button("Login", use_container_width=True, type="primary")
            
        if submitted:
            self._handle_login(phone_number, password)
    
    def _handle_login(self, phone_number: str, password: str):
        """Handle login form submission"""
        if not phone_number or not password:
            st.error("Please fill in all required fields.")
            return
            
        with st.spinner("Logging in..."):
            try:
                result = self.api_client.login_for_access_token(phone_number, password)
                if result and "access_token" in result:
                    st.session_state.access_token = result["access_token"]
                    self.api_client.set_auth_token(st.session_state.access_token)

                    # Fetch user profile
                    user_profile = self.api_client.read_users_me()
                    if user_profile:
                        st.session_state.user_data = user_profile
                        st.session_state.authenticated = True
                        st.success("Login successful! Redirecting...")
                        st.rerun()
                    else:
                        st.error("Failed to fetch user profile. Please try again.")
                else:
                    st.error("Invalid phone number or password. Please try again.")
            except Exception as e:
                logger.error(f"Login error: {e}")
                st.error("An error occurred during login. Please try again later.")
    
    def show_signup_page(self):
        """Display signup page with OTP verification"""
        st.header("📝 Create New Account")
        
        if st.session_state.signup_step == 1:
            self._show_otp_request_step()
        elif st.session_state.signup_step == 2:
            self._show_otp_verification_step()
    
    def _show_otp_request_step(self):
        """Show step 1: OTP request"""
        st.subheader("Step 1: Enter Phone Number")
        
        with st.form("send_otp_form"):
            phone_number = st.text_input(
                "Phone Number", 
                placeholder="Enter your phone number (e.g., +919876543210)",
                help="Enter a valid phone number to receive OTP"
            )
            
            submitted = st.form_submit_button("Send OTP", use_container_width=True, type="primary")

            if submitted and phone_number:
                self._send_otp(phone_number)
    
    def _send_otp(self, phone_number: str):
        """Send OTP to phone number"""
        with st.spinner("Sending OTP..."):
            try:
                if self.api_client.send_signup_otp(phone_number):
                    st.session_state.signup_phone_number = phone_number
                    st.session_state.signup_step = 2
                    st.success("OTP sent successfully! Please check your phone.")
                    st.rerun()
                else:
                    st.error("Failed to send OTP. Please check your phone number and try again.")
            except Exception as e:
                logger.error(f"OTP sending error: {e}")
                st.error("An error occurred while sending OTP. Please try again later.")
    
    def _show_otp_verification_step(self):
        """Show step 2: OTP verification and account creation"""
        st.subheader("Step 2: Verify OTP and Complete Registration")
        
        with st.form("verify_otp_form"):
            col1, col2 = self._create_signup_form_columns()
            
            # Form submission buttons
            col_verify, col_resend = st.columns([2, 1])
            with col_verify:
                submitted = st.form_submit_button("Verify OTP & Create Account", use_container_width=True, type="primary")
            with col_resend:
                resend_clicked = st.form_submit_button("Resend OTP", use_container_width=True)
            
            if submitted:
                self._handle_signup_verification()
            elif resend_clicked:
                self._resend_otp()
    
    def _create_signup_form_columns(self) -> tuple:
        """Create form columns for signup"""
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.text_input("Phone Number", value=st.session_state.signup_phone_number, disabled=True)
            self.otp_code = st.text_input("OTP Code", placeholder="Enter the 6-digit OTP")
            self.name = st.text_input("Full Name", value=st.session_state.signup_name, placeholder="Enter your full name")
            self.email = st.text_input("Email", value=st.session_state.signup_email, placeholder="Enter your email address")
            self.password = st.text_input("Password", type="password", value=st.session_state.signup_password, placeholder="Create a strong password")
            self.confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
            self.has_given_consent = st.checkbox("I agree to the terms and conditions", value=st.session_state.signup_consent)
        
        with col2:
            st.markdown("### Join Our Community! 🤝")
            st.markdown("Help preserve traditional Indian childhood games for future generations.")
            st.markdown("**Key Features:**")
            st.markdown("- 📸 Upload game photos and videos")
            st.markdown("- 📝 Document game rules and stories")
            st.markdown("- 🎵 Share traditional game songs")
            st.markdown("- 🏆 Build your contribution portfolio")
        
        return col1, col2
    
    def _handle_signup_verification(self):
        """Handle signup form verification and submission"""
        # Validation
        if not all([self.otp_code, self.name, self.email, self.password, self.confirm_password]):
            st.error("Please fill in all fields.")
            return
        
        if self.password != self.confirm_password:
            st.error("Passwords don't match.")
            return
        
        if self.password and len(self.password) < config.min_password_length:
            st.error(f"Password must be at least {config.min_password_length} characters long.")
            return
        
        if not self.has_given_consent:
            st.error("Please agree to the terms and conditions.")
            return
        
        # Save form data to session state
        st.session_state.signup_name = self.name
        st.session_state.signup_email = self.email
        st.session_state.signup_password = self.password
        st.session_state.signup_consent = self.has_given_consent

        # Verify OTP and create account
        with st.spinner("Verifying OTP and creating account..."):
            try:
                if self.api_client.verify_signup_otp(
                    phone=st.session_state.signup_phone_number,
                    otp=self.otp_code or "",
                    name=self.name or "",
                    email=self.email or "",
                    password=self.password or "",
                    consent=self.has_given_consent
                ):
                    st.success("Account created successfully! Please login with your credentials.")
                    st.balloons()
                    SessionStateManager.reset_signup()
                    st.rerun()
                else:
                    st.error("OTP verification failed or account creation error. Please check OTP and try again.")
            except Exception as e:
                logger.error(f"Signup verification error: {e}")
                st.error("An error occurred during account creation. Please try again later.")
    
    def _resend_otp(self):
        """Resend OTP to user"""
        with st.spinner("Resending OTP..."):
            try:
                if self.api_client.resend_signup_otp(st.session_state.signup_phone_number):
                    st.success("OTP re-sent successfully!")
                else:
                    st.error("Failed to resend OTP. Please try again.")
            except Exception as e:
                logger.error(f"OTP resend error: {e}")
                st.error("An error occurred while resending OTP. Please try again later.")

class MainApplication:
    """Main application handler"""
    
    def __init__(self, api_client: APIClientWrapper):
        self.api_client = api_client
        self.auth_handler = AuthenticationHandler(api_client)
    
    def run(self):
        """Run the main application"""
        # Initialize session state
        SessionStateManager.initialize()
        
        # Load styles
        StyleManager.load_styles()
        
        # Handle authentication token
        self._handle_existing_token()
        
        # Show main header
        self._show_header()
        
        # Route to appropriate view
        if not st.session_state.authenticated:
            self._show_authentication_view()
        else:
            self._show_authenticated_view()
    
    def _handle_existing_token(self):
        """Handle existing authentication token"""
        if st.session_state.access_token and not st.session_state.authenticated:
            self.api_client.set_auth_token(st.session_state.access_token)
            
            try:
                user_profile = self.api_client.read_users_me()
                if user_profile:
                    st.session_state.user_data = user_profile
                    st.session_state.authenticated = True
                    st.success("Re-authenticated successfully!")
                    st.rerun()
                else:
                    SessionStateManager.reset_auth()
                    st.warning("Session expired. Please log in again.")
            except Exception as e:
                logger.error(f"Token validation error: {e}")
                SessionStateManager.reset_auth()
    
    def _show_header(self):
        """Show application header"""
        st.markdown('<h1 class="main-header">మన ఆటలు (Mana Aatalu)</h1>', unsafe_allow_html=True)
        st.markdown('<p class="telugu-text" style="text-align: center;">Our Traditional Childhood Games - Preserving Cultural Heritage</p>', unsafe_allow_html=True)
        st.markdown("---")
    
    def _show_authentication_view(self):
        """Show authentication pages"""
        auth_tab = st.sidebar.selectbox("Choose Action", ["Login", "Sign Up"])
        
        if auth_tab == "Login":
            self.auth_handler.show_login_page()
        else:
            self.auth_handler.show_signup_page()
    
    def _show_authenticated_view(self):
        """Show main application for authenticated users"""
        self._show_sidebar_navigation()
        
        # Route to selected page
        page = st.session_state.get('selected_page', 'Home')
        
        if page == "Home":
            self._show_home_page()
        elif page == "Dashboard":
            self._show_dashboard()
        elif page == "Add New Game":
            self._show_add_content_page()
        elif page == "Profile":
            self._show_profile_page()
    
    def _show_sidebar_navigation(self):
        """Show sidebar navigation"""
        with st.sidebar:
            st.markdown('<div class="sidebar-logo">', unsafe_allow_html=True)
            st.markdown("### 🎮 Mana Aatalu")
            st.markdown(f"**Welcome, {st.session_state.user_data.get('full_name', 'User')}!**")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.session_state.selected_page = st.selectbox(
                "Navigate to:",
                ["Home", "Dashboard", "Add New Game", "Profile"]
            )
            
            st.markdown("---")
            
            if st.button("🚪 Logout", use_container_width=True):
                SessionStateManager.reset_auth()
                st.rerun()
    
    def _show_home_page(self):
        """Show home page"""
        st.header("Welcome to Mana Aatalu! 🎮")
        st.subheader("(మన ఆటలుకు స్వాగతం!)")
        
        # Mission and description
        with st.container():
            st.markdown("""
            **Mana Aatalu (మన ఆటలు)** is a community-driven platform dedicated to preserving and promoting 
            the traditional childhood games of India. In an era dominated by digital entertainment, many of 
            our rich cultural games are slowly fading away.
            
            ### Our Mission 🎯
            
            - **Preserve:** Document the rules, stories, and cultural context of traditional Indian games
            - **Promote:** Encourage the playing and learning of these games within families and communities  
            - **Connect:** Create a platform for enthusiasts to share their knowledge and memories
            
            ### What you can do here 🛠️
            
            - **Explore:** Discover games from different regions and categories
            - **Contribute:** Share your knowledge by adding new games, photos, and videos
            - **Connect:** Be part of a community passionate about cultural heritage
            """)
        
        # Telugu section
        with st.container():
            st.markdown("---")
            st.markdown("""
            <div class="telugu-text">
            <h3>మా లక్ష్యం</h3>
            <p>
            మన ఆటలు అనేది భారతదేశంలోని సాంప్రదాయ బాల్య క్రీడలను పరిరక్షించడానికి మరియు ప్రోత్సహించడానికి 
            అంకితం చేయబడిన ఒక కమ్యూనిటీ-ఆధారిత వేదిక. ఈ ప్రాజెక్ట్ ద్వారా కొత్త తరాలకు మన సాంస్కృతిక వారసత్వాన్ని 
            అందుబాటులోకి తీసుకురావాలని లక్ష్యంగా పెట్టుకుంది.
            </p>
            </div>
            """, unsafe_allow_html=True)
    
    def _show_dashboard(self):
        """Show user dashboard"""
        st.header("📊 Dashboard Overview")
        
        # User stats
        col1, col2 = st.columns(2)
        
        with col1:
            self._show_user_contributions_metric()
        
        with col2:
            st.markdown("""
            <div class="metric-container">
                <h3>Community</h3>
                <h2>🔒 N/A</h2>
                <p>Requires admin role to view</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Recent activity
        st.subheader("📈 Your Recent Contributions")
        self._show_recent_contributions()
    
    def _show_user_contributions_metric(self):
        """Show user contributions metric"""
        user_id = st.session_state.user_data.get('id')
        if not user_id:
            st.error("User ID not found")
            return
        
        try:
            total_contributions = 0
            media_types = ['text', 'audio', 'image', 'video']
            
            for media_type in media_types:
                response = self.api_client.get_user_contributions_by_media(user_id=user_id, media_type=media_type)
                if response and response.get('contributions'):
                    total_contributions += len(response['contributions'])
            
            st.markdown(f"""
            <div class="metric-container">
                <h3>Your Contributions</h3>
                <h2>📝 {total_contributions}</h2>
                <p>Games you've documented</p>
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            logger.error(f"Error fetching user contributions: {e}")
            st.error("Unable to load contribution statistics")
    
    def _show_recent_contributions(self):
        """Show recent user contributions"""
        user_id = st.session_state.user_data.get('id')
        if not user_id:
            st.info("Login to see your recent contributions.")
            return
        
        try:
            with st.spinner("Loading your recent contributions..."):
                all_contributions = []
                media_types = ['text', 'audio', 'image', 'video']
                
                for media_type in media_types:
                    response = self.api_client.get_user_contributions_by_media(user_id=user_id, media_type=media_type)
                    if response and response.get('contributions'):
                        all_contributions.extend(response['contributions'])
                
                if all_contributions:
                    # Sort by timestamp
                    all_contributions.sort(
                        key=lambda x: datetime.fromisoformat(x['timestamp'].replace('Z', '+00:00')) 
                        if x.get('timestamp') else datetime.min, 
                        reverse=True
                    )
                    
                    # Limit to recent contributions
                    recent_contributions = all_contributions[:config.max_recent_contributions]
                    
                    st.success(f"Found {len(recent_contributions)} recent contributions!")
                    
                    for contrib in recent_contributions:
                        self._display_contribution_card(contrib)
                else:
                    st.info("No contributions found. Be the first to add a game! 🎮")
                    
        except Exception as e:
            logger.error(f"Error loading contributions: {e}")
            st.error("Unable to load recent contributions")
    
    def _display_contribution_card(self, contrib: Dict[str, Any]):
        """Display a contribution card"""
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                game_name = contrib.get('title', 'Unknown Content')
                location_data = contrib.get('location', {})
                
                if location_data and location_data.get('latitude') and location_data.get('longitude'):
                    location_display = f"Lat: {location_data['latitude']}, Lon: {location_data['longitude']}"
                else:
                    location_display = "Not specified"
                
                st.markdown(f"**{game_name}**")
                st.caption(f"Location: {location_display} | Added by: {st.session_state.user_data.get('full_name', 'You')}")
            
            with col2:
                timestamp = contrib.get('timestamp', 'Recently')
                st.markdown(f"*{timestamp}*")
            
            st.markdown("---")
    
    def _show_add_content_page(self):
        """Show add content page"""
        st.header("➕ Add New Content")
        st.markdown("Help preserve our cultural heritage by documenting traditional content!")
        
        with st.form("add_content_form", clear_on_submit=True):
            self._create_content_form()
            
            submitted = st.form_submit_button("📤 Submit Content", use_container_width=True, type="primary")
            
            if submitted:
                self._handle_content_submission()
    
    def _create_content_form(self):
        """Create content submission form"""
        # Basic information
        st.subheader("📝 Content Information")
        self.title = st.text_input("Title *", placeholder="Enter a title for your content")
        self.description = st.text_area(
            "Short Description *", 
            placeholder=f"Provide a brief description (minimum {config.min_description_length} characters)", 
            height=100
        )
        self.content_text = st.text_area(
            "Detailed Content *", 
            placeholder="Enter your detailed text content here...", 
            height=150
        )
        
        # Category selection
        st.subheader("🏷️ Category")
        categories = self.api_client.get_categories()
        if categories:
            category_options = {cat['name']: cat['id'] for cat in categories if cat.get('name') and cat.get('id')}
            self.selected_category = st.selectbox("Category *", list(category_options.keys()))
            self.selected_category_id = category_options.get(self.selected_category)
        else:
            st.error("Unable to load categories. Please try again later.")
            self.selected_category_id = None
        
        # Location
        st.subheader("📍 Location (Optional)")
        col_lat, col_lon = st.columns(2)
        
        with col_lat:
            self.latitude = st.number_input("Latitude", format="%.6f", help="e.g., 17.3850")
        
        with col_lon:
            self.longitude = st.number_input("Longitude", format="%.6f", help="e.g., 78.4867")
        
        # Language and rights
        st.subheader("🌐 Language & Rights")
        self.language = st.selectbox(
            "Select Language *", 
            ["-- Select a language --", "Telugu", "English", "Hindi", "Other"]
        )
        
        release_rights_options = {
            "This work is created by me and anyone is free to use it.": "creator",
            "This work is created by my family/friends and I took permission to upload their work.": "family_or_friend",
            "I downloaded this from the internet and/or I don't know if it is free to share.": "downloaded"
        }
        
        self.release_rights_display = st.radio("Release Rights *", list(release_rights_options.keys()))
        self.release_rights = release_rights_options[self.release_rights_display]
    
    def _handle_content_submission(self):
        """Handle content form submission"""
        # Validation
        if not self._validate_content_form():
            return
        
        try:
            with st.spinner("Submitting your content..."):
                # Here you would implement the actual content submission logic
                # For now, this is a placeholder
                st.success("Content submitted successfully! 🎉")
                st.balloons()
                
        except Exception as e:
            logger.error(f"Content submission error: {e}")
            st.error("An error occurred while submitting content. Please try again later.")
    
    def _validate_content_form(self) -> bool:
        """Validate content submission form"""
        if not self.title:
            st.error("Please enter a title.")
            return False
        
        if not self.description or len(self.description) < config.min_description_length:
            st.error(f"Description must be at least {config.min_description_length} characters long.")
            return False
        
        if not self.content_text:
            st.error("Please enter detailed content.")
            return False
        
        if not self.selected_category_id:
            st.error("Please select a category.")
            return False
        
        if self.language == "-- Select a language --":
            st.error("Please select a language.")
            return False
        
        return True
    
    def _show_profile_page(self):
        """Show user profile page"""
        st.header("👤 User Profile")
        
        user_data = st.session_state.user_data
        if not user_data:
            st.error("User data not found. Please log in again.")
            return
        
        # Display user information
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("Profile Information")
            st.write(f"**Name:** {user_data.get('full_name', 'N/A')}")
            st.write(f"**Phone:** {user_data.get('phone', 'N/A')}")
            st.write(f"**User ID:** {user_data.get('id', 'N/A')}")
        
        with col2:
            st.subheader("Account Settings")
            st.info("Profile editing features will be available soon!")
            
            if st.button("🔄 Refresh Profile"):
                try:
                    updated_profile = self.api_client.read_users_me()
                    if updated_profile:
                        st.session_state.user_data = updated_profile
                        st.success("Profile refreshed successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to refresh profile.")
                except Exception as e:
                    logger.error(f"Profile refresh error: {e}")
                    st.error("An error occurred while refreshing profile.")

def main():
    """Main application entry point"""
    # Page configuration
    st.set_page_config(
        page_title=config.page_title,
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize and run application
    api_client = get_api_client()
    app = MainApplication(api_client)
    app.run()

if __name__ == "__main__":
    main()