import subprocess
import time
import sys
import os
from datetime import datetime

# Path to your main script
MQTT_SCRIPT = "Mqtthings.py"  # <-- Change to the name of the file you want to supervise

# Path to the log file
LOG_FILE = "main.log"

def write_log(message: str):
    """
    Appends a timestamped message to the supervisor log file.
    """
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now()} - {message}\n")

def run_script():
    """
    Runs the MQTT script in a subprocess and returns when it exits.
    """
    process = subprocess.Popen([sys.executable, MQTT_SCRIPT])
    # Wait for the child process to finish
    process.wait()
    return process.returncode

def main():
    while True:
        # Log the script start
        start_msg = f"Starting {MQTT_SCRIPT}..."
        print(start_msg)
        write_log(start_msg)

        exit_code = run_script()

        # Log the script end
        end_msg = f"{MQTT_SCRIPT} ended with exit code {exit_code}."
        print(end_msg)
        write_log(end_msg)

        # Wait 60 seconds before restarting
        waiting_msg = "Waiting 60 seconds before restarting..."
        print(waiting_msg)
        write_log(waiting_msg)

        time.sleep(60)

if __name__ == "__main__":
    main()
