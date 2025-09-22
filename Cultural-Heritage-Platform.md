# Overview

The Indian Cultural Heritage Collection Platform is a Streamlit-based web application designed to collect, preserve, and share India's rich linguistic and cultural diversity. The platform serves as a crowdsourced repository where users can contribute stories, proverbs, traditional recipes, and landmark information in multiple Indian languages. The application operates with an offline-first architecture, allowing users to contribute content even when internet connectivity is limited, with automatic synchronization when connection is restored.

The platform supports multilingual content collection across major Indian languages including Hindi, Tamil, Telugu, Bengali, Marathi, Gujarati, Kannada, Malayalam, Punjabi, Odia, and Urdu, complete with native scripts and proper language detection. Users can contribute through various media types including text, audio recordings, and images, making cultural preservation accessible through multiple input methods.

# Recent Changes

## Migration to Replit Environment - August 30, 2025
- ✅ Successfully migrated from Replit Agent to native Replit environment
- ✅ Installed all required Python dependencies (Streamlit, OpenAI, Plotly, etc.)
- ✅ Configured Streamlit server on port 5000 with proper settings
- ✅ Updated authentication system to support AI API integration
- ✅ Added phone-based authentication with API fallback to local database
- ✅ Created proper `.streamlit/secrets.toml` and `.streamlit/config.toml` configuration
- ✅ Fixed database schema issues and LSP errors
- ✅ Application now running successfully at http://0.0.0.0:5000

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
The application uses Streamlit as the primary web framework with a multi-page application structure. The main entry point (`app.py`) handles authentication flow and routing, while individual pages are organized under the `pages/` directory for different content types (Stories & Proverbs, Recipe Exchange, Landmark Collection, Analytics, Profile).

The UI is built with reusable components located in the `components/` directory, including specialized modules for audio recording (`audio_recorder.py`), image uploading (`image_uploader.py`), and language selection (`language_selector.py`). The interface is bilingual with Hindi/English support throughout.

## Backend Architecture  
The backend follows a service-oriented architecture with separation of concerns through dedicated service classes:

- **AuthService**: Handles user authentication via OTP-based phone verification
- **APIClient**: Manages HTTP communication with external Indic Corpus Collections API
- **AIService**: Provides AI-powered content analysis including language detection and audio transcription using OpenAI and Hugging Face models
- **OfflineStorage**: Manages local SQLite database for offline functionality

## Data Storage Solutions
The application implements a dual storage strategy:

**Local Storage (SQLite)**: Primary storage managed through `SQLiteManager` class with comprehensive schema including users, records, media files, and sync queues. The local database handles offline functionality and serves as a buffer for content before API synchronization.

**Remote Storage**: Integration with external Indic Corpus Collections API for centralized data persistence and cross-platform data sharing.

The offline-first design ensures users can contribute content without internet connectivity, with automatic background synchronization when connection is restored.

## Authentication and Authorization
Authentication uses OTP-based phone verification through the external API. The system maintains JWT tokens for session management with automatic refresh capabilities. Session state is managed through Streamlit's built-in session management, storing user credentials, authentication status, and user preferences locally.

## AI and Content Processing
The platform integrates multiple AI services for content enhancement:

- **Language Detection**: Automatic language identification using Hugging Face transformers
- **Audio Transcription**: Whisper model integration for converting audio content to text
- **Content Analysis**: OpenAI API integration for content categorization and metadata extraction

These AI capabilities enhance the user experience by automatically detecting content language and converting multimedia inputs into searchable text formats.

# External Dependencies

## Third-party APIs
- **Indic Corpus Collections API**: External backend API hosted at `https://api.viswam.ai` providing authentication services and centralized data storage
- **OpenAI API**: Used for advanced content analysis and natural language processing tasks
- **Hugging Face API**: Provides language detection models and other NLP capabilities

## Python Libraries
- **Streamlit**: Core web framework for UI rendering and user interaction
- **Streamlit-Option-Menu**: Enhanced navigation components for better user experience
- **OpenAI**: Official OpenAI Python client for GPT integration
- **Transformers**: Hugging Face library for machine learning model integration
- **Whisper**: OpenAI's speech recognition model for audio transcription
- **Pillow**: Image processing and manipulation library
- **PyAudio**: Audio recording functionality for voice contributions
- **Requests**: HTTP client for API communication
- **SQLite3**: Local database management for offline storage

## Audio/Visual Processing
- **PyAudio**: Real-time audio recording capabilities
- **Wave**: Audio file format handling
- **Pillow (PIL)**: Image processing, resizing, and format conversion
- **Plotly**: Interactive data visualization for analytics dashboard

## Development Tools
- **UUID**: Unique identifier generation for records and users
- **DateTime**: Timestamp management and date/time operations
- **JSON**: Data serialization for API communication and local storage
- **Base64**: Media file encoding for storage and transmission
