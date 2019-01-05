# Rename Images with Date Photo Taken

# Purpose: Renames image files in a folder based on date photo taken from EXIF metadata

# Author: Matthew Renze

# Usage: python.exe Rename.py input-folder
#   - input-folder = the directory containing the image files to be renamed

# Example: python.exe Rename.py C:\Photos

# Behavior:
# Given a photo named "Photo Apr 01, 5 54 17 PM.jpg"  
# with EXIF date taken of "4/1/2018 5:54:17 PM"  
# when you run this script on its parent folder
# then it will be renamed "20180401-175417.jpg"

# Notes:
#   - For safety, please make a backup before running this script
#   - Currently only designed to work with .jpg, .jpeg, and .png files
#   - EXIF metadata must exist or an error will occur

# Import libraries
import os
import sys
from PIL import Image

# Set list of valid file extensions
valid_extensions = [".jpg", ".jpeg", ".png"]

# Get folder path from arguments
folder_path = input_file_path = sys.argv[1]

# Get all files from folder
file_names = os.listdir(folder_path)

# For each file
for file_name in file_names:

    # Get the file extension
    file_ext = os.path.splitext(file_name)[1]

    # If the file does not have a valid file extension
    # then skip it
    if (file_ext not in valid_extensions):
        continue

    # Create the old file path
    old_file_path = os.path.join(folder_path, file_name)

    # Open the image
    image = Image.open(old_file_path)

    # Get the date taken from EXIF metadata
    date_taken = image._getexif()[36867]

    # Close the image
    image.close()

    # Reformat the date taken to "YYYYMMDD-HHmmss"
    date_time = date_taken \
        .replace(":", "")      \
        .replace(" ", "-")

    # Combine the new file name and file extension
    new_file_name = date_time + file_ext

    # Create the new folder path
    new_file_path = os.path.join(folder_path, new_file_name)

    # Rename the file
    os.rename(old_file_path, new_file_path)



