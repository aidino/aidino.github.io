#!/bin/bash

# Check if a folder path is provided as an argument
if [ $# -ne 1 ]; then
  echo "Usage: $0 <folder_path>"
  exit 1
fi

folder_path="$1"
output_file="stories_vi.txt"

# Check if the folder exists
if [ ! -d "$folder_path" ]; then
  echo "Error: Folder '$folder_path' not found."
  exit 1
fi

# Combine all .txt files in the folder into the output file
cat "$folder_path"/*.txt > "$output_file"

# Check if the combination was successful
if [ $? -eq 0 ]; then
  echo "Successfully combined all .txt files in '$folder_path' into '$output_file'."
else
  echo "Error: Failed to combine .txt files."
  exit 1
fi