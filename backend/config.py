import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env if present
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

class Config:
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '').strip()
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '').strip()
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = os.getenv('DEBUG', 'True').lower() in ('true', '1', 't')
    
    # Model preferences
    GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')

    # Preset templates for quick demo and testing
    PRESETS = [
        {
            "id": "todo-app",
            "title": "Full-Stack Task Manager (Flask + SQLite + Glassmorphism UI)",
            "prompt": "Build a responsive modern full-stack Task Management application using Python Flask, SQLite database, and an ultra-modern dark UI with category tags, due dates, priority filters, and REST API endpoints."
        },
        {
            "id": "weather-dashboard",
            "title": "Interactive Weather Analytics Dashboard",
            "prompt": "Create an interactive Weather Analytics dashboard web app using HTML5, CSS3, JavaScript, and Python backend that displays 7-day forecast cards, temperature charts, animated weather icons, and city search with caching."
        },
        {
            "id": "url-shortener",
            "title": "Custom URL Shortener & Analytics API",
            "prompt": "Develop a high-performance URL Shortener service with click analytics, QR code generation, expiration timestamps, and a sleek web dashboard using Python and JavaScript."
        },
        {
            "id": "markdown-note-app",
            "title": "Real-time Markdown Notes & Knowledge Base",
            "prompt": "Build a Markdown Notes and Knowledge Base web app with live preview, syntax highlighting, tag-based search, local storage sync, and PDF/HTML export capabilities."
        }
    ]
