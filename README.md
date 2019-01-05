# Rename Images with Date Photo Taken

Purpose: Renames image files in a folder based on date photo taken from EXIF metadata

Author: Matthew Renze

Usage: python.exe Rename.py input-folder
  - input-folder = the directory containing the image files to be renamed

Example: python.exe Rename.py C:\Photos

Notes:
  - For safety, please make a backup before running this script
  - Currently only designed to work with .jpg, .jpeg, and .png files
  - EXIF metadate must exist or an error will occur
