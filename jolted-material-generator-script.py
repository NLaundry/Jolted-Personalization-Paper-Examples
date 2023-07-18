import os
import time
import subprocess
import logging
from itertools import product

# Define inputs
topics = ["loops in python", "linked lists in python", "asynchronous programming in python"]
levels_of_expertise = ["beginner student", "intermediate student", "expert in other programming languages but learning python"]
educational_backgrounds = ["videogame design", "psychology", "full-stack web development"]
model = "gpt-4"  # replace with your model name

# Set up logging
logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(message)s')

# Generate all combinations of topics, levels of expertise, and educational backgrounds
combinations = list(product(topics, levels_of_expertise, educational_backgrounds))
# Add default combinations
default_combinations = [(topic, "computer science student", "computer science") for topic in topics]
combinations.extend(default_combinations)

# Load last successful command from log file
try:
    with open('log.txt', 'r') as f:
        last_success = f.readlines()[-1].strip()
        last_success_index = combinations.index(eval(last_success))
        combinations = combinations[last_success_index+1:]
except (FileNotFoundError, IndexError, ValueError):
    pass  # Continue with all combinations if log file is empty or does not exist

# Run command for all combinations
for topic, level, background in combinations:
    # Escape characters and spaces in inputs
    safe_topic = topic.replace(" ", "\\ ")
    safe_level = level.replace(" ", "\\ ")
    safe_background = background.replace(" ", "\\ ")

    while True:
        try:
            # Run command
            command = f"jolted-cli create-notebook --topic {safe_topic} --educational-background {safe_background} --level-of-expertise {safe_level} --model {model}"
            subprocess.run(command, shell=True, check=True)

            # Determine old and new file names
            old_file_name = f"{topic}.ipynb"  # replace with your file naming scheme
            new_file_name = f"{topic}_{level}_{background}.ipynb"

            # Rename file
            os.rename(old_file_name, new_file_name)

            # Log successful command
            logging.info((topic, level, background))

            # Break the loop if the command executed successfully
            break

        except subprocess.CalledProcessError:
            print("Command failed. Waiting for 1 minute before retrying...")
            time.sleep(60)  # Wait for 1 minute
