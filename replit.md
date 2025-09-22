# Overview

The Indian Cultural Heritage Collection Platform is a multilingual web application designed to collect, preserve, and share India's rich linguistic and cultural diversity. The platform enables users to contribute various forms of cultural content including stories, proverbs, traditional recipes, landmarks, and multimedia content across major Indian languages. The system supports both Flask-based web interface and Streamlit-based components for content management and submission.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
The application uses a hybrid approach with Flask as the primary web framework and Streamlit components for specialized content submission workflows. The Flask frontend follows a traditional template-based architecture with Bootstrap for responsive design and multi-language support through template-based internationalization.

The UI is structured with:
- **Base Template System**: Centralized layout with navigation, language switching, and user authentication states
- **Multi-language Support**: Template-based translations covering Hindi, Tamil, Telugu, Bengali, Marathi, Gujarati, Kannada, Malayalam, Punjabi, Odia, Urdu, and Assamese
- **Responsive Design**: Bootstrap-based UI with custom CSS for cultural theming
- **Component-based Forms**: Specialized forms for different content types (stories, recipes, landmarks)

## Backend Architecture
The backend implements a service-oriented architecture with clear separation between Flask web routes and API integration services:

- **Flask Application**: Handles user authentication, session management, and web interface routing
- **API Integration Layer**: Manages communication with external Indic Corpus Collections API for data persistence
- **Authentication Service**: OTP-based phone verification with JWT token management
- **Content Management**: Specialized handlers for different media types (text, audio, video)

The architecture supports both online API-based operations and offline functionality through local storage mechanisms.

## Data Storage Solutions
The platform implements a dual-storage strategy:

**Primary Storage**: Integration with external Indic Corpus Collections API (`https://api.corpus.swecha.org/api/v1`) for centralized data persistence and cross-platform compatibility.

**Local Storage**: SQLite-based offline storage for scenarios where API connectivity is unavailable, with automatic synchronization capabilities when connection is restored.

**Session Management**: Flask-based session handling with secure token management for authenticated users.

## Authentication and Authorization
The system uses phone-number-based authentication with OTP verification:

- **Primary Authentication**: OTP-based phone verification through external API
- **Session Management**: Flask-Login integration with JWT tokens for persistent sessions
- **Multi-modal Login**: Support for both password-based and OTP-based authentication methods
- **User Profiles**: Comprehensive user management with cultural contribution tracking

# External Dependencies

## Core APIs
- **Indic Corpus Collections API**: Primary data storage and retrieval service for cultural content submissions
- **OpenAI API**: AI-powered content analysis, language detection, and audio transcription services
- **Hugging Face Models**: Additional AI capabilities for multilingual content processing

## Third-party Services
- **Streamlit**: Alternative interface for specialized content submission workflows
- **Bootstrap 5**: Frontend UI framework for responsive design
- **Font Awesome**: Icon library for enhanced user interface
- **Flask-Login**: User session management and authentication
- **WTForms**: Form handling and validation

## Development Tools
- **SQLite**: Local database for offline functionality
- **Plotly**: Data visualization for user contribution analytics
- **Requests**: HTTP client for API communications

## Language and Localization
- **Multi-language Template System**: Native support for 13 Indian languages with proper Unicode handling
- **Cultural Theming**: Custom CSS with Indian cultural color schemes and design elements