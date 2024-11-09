
# Rename Images and Videos with Date Taken or Creation Date

# Purpose: Renames image and video files in a folder based on date photo taken (from EXIF metadata) or video creation date.

# Author: Matthew Renze
# Update: 20241109 Added support for video files. Arcadehacker

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
#   - Currently only designed to work with .jpg, .jpeg, .png, mp4, .mov, and .avi files
#   - If you omit the input folder, then the current working directory will be used instead.

# Import libraries
import os
import sys
from datetime import datetime
from PIL import Image
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser

# Set list of valid file extensions for images and videos
image_extensions = [".jpg", ".jpeg", ".png"]
video_extensions = [".mp4", ".mov", ".avi"]
all_extensions = image_extensions + video_extensions

# Function to get the date from image EXIF data
def get_image_date(filepath):
    try:
        img = Image.open(filepath)
        exif_data = img._getexif()
        if exif_data:
            # EXIF DateTimeOriginal tag
            date_str = exif_data.get(36867)
            if date_str:
                return datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
    except Exception as e:
        print(f"Error retrieving image date: {e}")
    return None

# Function to get the date from video metadata
def get_video_date(filepath):
    try:
        parser = createParser(filepath)
        if not parser:
            print(f"Unable to parse video file: {filepath}")
            return None
        metadata = extractMetadata(parser)
        if metadata and metadata.has("creation_date"):
            return metadata.get("creation_date")
    except Exception as e:
        print(f"Error retrieving video date: {e}")
    return None

# Main function to rename files based on extracted date
def rename_files(input_folder):
    for root, _, files in os.walk(input_folder):
        for filename in files:
            ext = os.path.splitext(filename)[1].lower()
            if ext in all_extensions:
                filepath = os.path.join(root, filename)

                # Get date based on file type
                if ext in image_extensions:
                    date = get_image_date(filepath)
                elif ext in video_extensions:
                    date = get_video_date(filepath)
                else:
                    continue

                # If a date was found, rename the file
                if date:
                    new_name = date.strftime("%Y%m%d-%H%M%S") + ext
                    new_filepath = os.path.join(root, new_name)

                    # Rename file only if the new name is different
                    if new_filepath != filepath:
                        os.rename(filepath, new_filepath)
                        print(f"Renamed '{filename}' to '{new_name}'")
                    else:
                        print(f"File '{filename}' already named correctly")
                else:
                    print(f"No date metadata found for '{filename}'")

# Entry point
if __name__ == "__main__":
    input_folder = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    rename_files(input_folder)
