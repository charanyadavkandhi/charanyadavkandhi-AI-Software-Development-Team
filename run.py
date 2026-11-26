"""
AI Software Development Team (Multi-Agent)
Capstone Project Launcher
School of CS&AI - Team 189
"""
import sys
import os

# Add current project root to python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from backend.app import app
from backend.config import Config

if __name__ == '__main__':
    print("=" * 70)
    print("[AI SOFTWARE DEVELOPMENT TEAM (MULTI-AGENT) - CAPSTONE SYSTEM]")
    print(f"[+] Server running at: http://localhost:{Config.PORT}")
    print("=" * 70)
    app.run(host='0.0.0.0', port=Config.PORT, debug=Config.DEBUG)
