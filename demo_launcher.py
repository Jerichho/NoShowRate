#!/usr/bin/env python3
"""
Demo Launcher for Airline No-Show Prediction
This script launches the complete demo environment
"""

import os
import sys
import subprocess
import webbrowser
import time
import threading

def start_app():
    """Start the Flask application."""
    print("Starting Flask application...")
    subprocess.run([sys.executable, 'app.py'])

def open_browser():
    """Open the web browser after a delay."""
    time.sleep(3)
    print("Opening web browser...")
    webbrowser.open('http://localhost:8080')

def main():
    print("=" * 60)
    print("AIRLINE NO-SHOW PREDICTION - DEMO LAUNCHER")
    print("=" * 60)
    print()
    print("This will start the web application and open it in your browser.")
    print("Press Ctrl+C to stop the demo.")
    print()
    
    # Start the Flask app in a separate thread
    app_thread = threading.Thread(target=start_app)
    app_thread.daemon = True
    app_thread.start()
    
    # Open browser after delay
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nDemo stopped. Thank you!")
        sys.exit(0)

if __name__ == "__main__":
    main()
