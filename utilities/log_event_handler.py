import logging
import os
import sys


def log():
    # Create the root logger
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler(sys.stdout)

    console_handler.setLevel(logging.INFO)

    log_file_path = os.path.abspath(os.path.join("..", "logs", "logs.log"))

    file_handler = logging.FileHandler(log_file_path, mode="a", delay=True)

    file_handler.setLevel(logging.DEBUG)

    # Define a log message format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add both handlers to the root logger
    root.addHandler(console_handler)
    root.addHandler(file_handler)

    return root


log_event = log()
