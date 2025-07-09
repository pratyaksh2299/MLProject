import logging  # Python module for logging messages to files or console
import os       # Module to work with file system paths and directories
from datetime import datetime  # To generate timestamps for log filenames

# Create a log file name using current date and time (month_day_year_hour_min_sec)
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Set the folder where log files will be saved ('logs' folder inside current working directory)
logs_dir = os.path.join(os.getcwd(), "logs")

# Create the logs directory if it doesn't already exist
os.makedirs(logs_dir, exist_ok=True)




# Full path where the log file will be saved (example: /your_path/logs/07_09_2025_16_55_30.log)
LOG_FILE_PATH = os.path.join(logs_dir, LOG_FILE)

# Setup the logging configuration:
# - filename: where to save logs
# - format: how log messages will look (time, line number, logger name, level, message)
# - level: INFO means log all messages from INFO and above (INFO, WARNING, ERROR, CRITICAL)
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


