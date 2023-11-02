import subprocess
import time
import logging

# Specify the path to your Python script
script_path = "Mqtthings.py"

# Define the Linux command you want to execute
command = "sudo systemctl restart thingsboard"

# Set up logging
logging.basicConfig(filename="main.log", level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

while True:
    # Log a message before running the script
    logging.info("Running Mqtthings.py...")
    
    # Run the script as a separate process and wait for it to finish
    process = subprocess.Popen(["python3", script_path])
    process.wait()
    
    # Log a message after running the script
    logging.info("Mqtthings.py execution finished.")
    
    # Log a message before restarting ThingsBoard
    logging.info("Restarting ThingsBoard...")
    
    # Run the command
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Log the result
    if result.returncode == 0:
        logging.info("Command executed successfully. Output:")
        logging.info(result.stdout)
    else:
        logging.error(f"Command failed with error:\n{result.stderr}")
    
    # Log a message after restarting ThingsBoard
    logging.info("ThingsBoard restart finished.")
    
    # Sleep for 5 minutes (300 seconds)
    time.sleep(300)
