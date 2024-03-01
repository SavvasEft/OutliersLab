import logging
import os

from datetime import datetime
from logging.handlers import RotatingFileHandler

logger_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(logger_dir, '..', '..', 'logs')
log_file = 'anomaly_detection_tool_logs.log'
full_log_file_path = os.path.join(log_dir, log_file) 

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

max_log_size = 5 * 1024 * 1024 #5 mb max log file

#Create logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

#Create formatter
formatter = logging.Formatter('%(asctime)s %(msecs)d- %(process)d-%(levelname)s - %(message)s', 
                              datefmt='%d-%b-%y %H:%M:%S %p')

# Set up the rotating file handler
handler = RotatingFileHandler(full_log_path, maxBytes=max_log_size, backupCount=backup_count, mode='a')
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)