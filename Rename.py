# Rename Images with Date Photo Taken

# Purpose: Renames image files in a folder based on date photo taken from EXIF metadata

# Author: Matthew Renze

# Usage: python.exe rename.py input-folder
#   - input-folder = (optional) the directory containing the image files to be renamed

# Examples: python.exe rename.py C:\Photos
#           python.exe rename.py

# Behavior:
#  - Given a photo named "Photo Apr 01, 5 54 17 PM.jpg"  
#  - with EXIF date taken of "4/1/2018 5:54:17 PM"  
#  - when you run this script on its parent folder
#  - then it will be renamed "20180401-175417.jpg"

# Notes:
#   - For safety, please make a backup of your photos before running this script
#   - Currently only designed to work with .jpg, .jpeg, and .png files
#   - If you omit the input folder, then the current working directory will be used instead.

# Import libraries
import os
import sys
from datetime import datetime
from PIL import Image

# Set list of valid file extensions
valid_extensions = [".jpg", ".JPG", ".jpeg", ".JPEG", ".png", ".PNG"]

# If folder path argument exists then use it
# Else use the current running folder
if len(sys.argv) > 1:
    folder_path = input_file_path = sys.argv[1]
else:
    folder_path = os.getcwd()

# Get all files from folder
file_names = os.listdir(folder_path)

# For each file
for file_name in file_names:

    # Get the file extension
    file_ext = os.path.splitext(file_name)[1]

    # Skip files without a valid file extension
    if (file_ext not in valid_extensions):
        continue

    # Create the old file path
    old_file_path = os.path.join(folder_path, file_name)

    # Open the image
    image = Image.open(old_file_path)

    # Get the EXIF metadata
    metadata = image._getexif()

    # Check if the metadata exists
    if metadata is None:
        print(f"EXIF metadata not found in file: {file_name}")
        continue

    # Get the date taken from the metadata
    if 36867 in metadata.keys():
        date_taken = metadata[36867]
    elif 306 in metadata.keys():
        date_taken = metadata[306]
    else:
        print(f"Date not found in file: {file_name}")
        continue

    # Close the image
    image.close()

    # Get the date taken as a datetime object
    date_taken = datetime.strptime(date_taken, "%Y:%m:%d %H:%M:%S")

    # Reformat the date taken to "YYYYMMDD-HHmmss"
    # NOTE: Change this line to change the date/time format of the output filename
    date_time = date_taken.strftime("%Y%m%d-%H%M%S")
    
    # Combine the new file name and file extension
    new_file_name = date_time + file_ext

    # Create the new folder path
    new_file_path = os.path.join(folder_path, new_file_name)

    # Rename the file
    os.rename(old_file_path, new_file_path)
