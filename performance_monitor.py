import psutil
import time
import datetime
import logging
import csv
import os

# --- Configuration ---
# Read from environment variables if set, otherwise use defaults
LOG_INTERVAL_SECONDS = int(os.getenv('LOG_INTERVAL_SECONDS', 5))
LOG_FILE_NAME = os.getenv('LOG_FILE_NAME', 'system_performance.csv')
# For LOG_DIRECTORY, if it's an empty string from env, treat it as None or the default
env_log_directory = os.getenv('LOG_DIRECTORY')
LOG_DIRECTORY = env_log_directory if env_log_directory and env_log_directory.strip() else 'performance_logs'


# --- Setup Logging ---
def setup_logging(log_file_path_param): # Renamed parameter to avoid conflict
    """Configures the CSV logger."""
    # Determine the final log file path
    # If LOG_DIRECTORY is set, join it with LOG_FILE_NAME
    # Otherwise, use LOG_FILE_NAME directly (logs in WORKDIR /app)
    if LOG_DIRECTORY:
        # Ensure the directory path is absolute within the container if mounted,
        # or relative to WORKDIR if not. For simplicity, we'll assume it's relative to WORKDIR.
        effective_log_dir = os.path.join(os.getcwd(), LOG_DIRECTORY) # /app/performance_logs
        os.makedirs(effective_log_dir, exist_ok=True)
        final_log_file_path = os.path.join(effective_log_dir, LOG_FILE_NAME)
    else:
        # Logs directly in /app if LOG_DIRECTORY is not set or is empty
        final_log_file_path = os.path.join(os.getcwd(), LOG_FILE_NAME)

    file_exists = os.path.isfile(final_log_file_path)

    logger = logging.getLogger('performance_monitor')
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        fh = logging.FileHandler(final_log_file_path)
        if not file_exists or os.path.getsize(final_log_file_path) == 0:
            with open(final_log_file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Timestamp', 'CPU Usage (%)', 'Memory Usage (%)'])
        logger.addHandler(fh)

    return logger, final_log_file_path


def get_cpu_usage():
    """Fetches the current system-wide CPU utilization."""
    # When running in Docker, cpu_percent might need `interval` to be non-zero
    # to get a non-zero reading, especially on the first call.
    return psutil.cpu_percent(interval=1) # interval=1 is already in your original script

def get_memory_usage():
    """Fetches the current virtual memory utilization."""
    memory = psutil.virtual_memory()
    return memory.percent

def log_performance_data(logger, log_file_path_param): # Renamed parameter
    """Retrieves performance data and logs it to the CSV file."""
    try:
        cpu_usage = get_cpu_usage()
        memory_usage = get_memory_usage()
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with open(log_file_path_param, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, cpu_usage, memory_usage])

        print(f"{timestamp} - CPU: {cpu_usage}%, Memory: {memory_usage}%")

    except Exception as e:
        logging.error(f"Error collecting or logging data: {e}")
        print(f"Error logging: {e}") # Also print to stdout for visibility in docker logs


if __name__ == "__main__":
    # Determine the log file path based on configuration
    if LOG_DIRECTORY:
        # We expect LOG_DIRECTORY to be relative to the WORKDIR (/app)
        # The setup_logging function will handle creating it.
        log_dir_path = LOG_DIRECTORY # e.g., "performance_logs"
        # The actual path for setup_logging will be constructed inside it.
        # For initial print message:
        expected_log_path_display = os.path.join(log_dir_path, LOG_FILE_NAME)
    else:
        expected_log_path_display = LOG_FILE_NAME

    print("Starting System Performance Monitor (inside Docker)...")
    print(f"Logging data every {LOG_INTERVAL_SECONDS} seconds.")
    print(f"Logs will be written to '{expected_log_path_display}' inside the container.")
    print("To access logs on the host, use a volume mount (see docker run command).")
    print("Press Ctrl+C on the host to stop the container (if running in foreground).")

    # The actual path construction is now centralized in setup_logging
    # We pass a "base name" or a relative path for the log file which setup_logging will resolve
    # For Docker, it's simpler if setup_logging always uses paths relative to WORKDIR or absolute paths.
    # Let setup_logging determine the full path.
    logger, configured_log_path = setup_logging(LOG_FILE_NAME) # Pass base name, setup_logging will use LOG_DIRECTORY

    try:
        while True:
            log_performance_data(logger, configured_log_path)
            time.sleep(LOG_INTERVAL_SECONDS)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user (KeyboardInterrupt received in container).")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        print(f"Performance logs were being saved to '{configured_log_path}' (inside container)")
        if logger and logger.handlers:
            for handler in logger.handlers:
                handler.close()
                logger.removeHandler(handler)