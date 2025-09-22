#!/usr/bin/env python3
"""
Standalone runner for the Cultural Heritage Platform
This file helps run the application outside of Replit environment
"""

import os
import sys
import subprocess
from pathlib import Path

def setup_environment():
    """Set up the environment for running outside Replit"""
    
    # Add current directory to Python path
    current_dir = Path(__file__).parent.absolute()
    if str(current_dir) not in sys.path:
        sys.path.insert(0, str(current_dir))
    
    # Create .streamlit directory if it doesn't exist
    streamlit_dir = current_dir / ".streamlit"
    streamlit_dir.mkdir(exist_ok=True)
    
    # Create config.toml if it doesn't exist
    config_file = streamlit_dir / "config.toml"
    if not config_file.exists():
        config_content = """[server]
headless = true
address = "0.0.0.0"
port = 8501

[browser]
gatherUsageStats = false
"""
        with open(config_file, 'w') as f:
            f.write(config_content)
    
    print("✅ Environment setup complete")

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import streamlit
        import requests
        import pandas
        import plotly
        import PIL
        print("✅ All required dependencies are available")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install dependencies using: pip install -r requirements.txt")
        return False

def run_streamlit():
    """Run the Streamlit application"""
    try:
        # Change port to 8501 (default Streamlit port) for local development
        os.environ.setdefault('STREAMLIT_SERVER_PORT', '8501')
        
        cmd = [
            sys.executable, "-m", "streamlit", "run", "src/app.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0"
        ]
        
        print("🚀 Starting Streamlit application...")
        print("📱 Open your browser to: http://localhost:8501")
        
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error running application: {e}")

if __name__ == "__main__":
    print("🎮 Cultural Heritage Platform - Standalone Runner")
    print("="*50)
    
    setup_environment()
    
    if check_dependencies():
        run_streamlit()
    else:
        print("\n📥 To install dependencies, run:")
        print("   pip install -r requirements.txt")