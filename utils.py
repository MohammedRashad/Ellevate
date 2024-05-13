import os 
import logging
from datetime import datetime

def list_files(directory):
    """
    The function `list_files` takes a directory path as input, retrieves all file paths within that
    directory and its subdirectories, processes each file path using a lambda function (in this case,
    simply returning it), and returns a list of processed file paths.
    
    :param directory: The `list_files` function you provided takes a directory path as input and returns
    a list of processed file paths within that directory
    :return: A list of processed file paths is being returned.
    """
    abs_directory = os.path.abspath(directory)
    file_paths = []  # List to store file paths
    for root, dirs, files in os.walk(abs_directory):
        for file in files:
            file_path = os.path.join(root, file)
            # Process the file path using a lambda, here simply returning it
            processed_path = (lambda x: x)(file_path)
            file_paths.append(processed_path)
    return file_paths


# Configure logging
logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def log_message(part1, part2):
    """Log a message composed of two string parts with a timestamp."""
    message = f"{part1} - {part2}"
    logging.info(message)

# # Example usage of the log_message function
# log_message("Part 1 of the log", "Part 2 of the log")
