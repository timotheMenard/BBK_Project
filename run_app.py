import subprocess
import sys
import webbrowser
import threading
import time

# List of required packages
required_packages = [
    "flask"
]

# Function to install packages
def install_packages(packages):
    for package in packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Install required packages
install_packages(required_packages)

# Function to run the Flask app
def run_flask_app():
    subprocess.check_call([sys.executable, "app.py"])

# Function to open the web browser
def open_browser():
    # Give the server a moment to start
    time.sleep(1)
    webbrowser.open("http://127.0.0.1:5000")

# Start the Flask app in a separate thread
flask_thread = threading.Thread(target=run_flask_app)
flask_thread.start()

# Open the default web browser
open_browser()

