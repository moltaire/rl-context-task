#!/bin/bash
# make-movie-stims.sh
# This script processes all .png files in specified subdirectories and
# creates animated MP4 files in an "anim" subfolder within each directory.

# List the subdirectories to process (change these names as needed)
subdirs=("Set 1" "Set 2")

for subdir in "${subdirs[@]}"; do
    # Check if the subdirectory exists
    if [ ! -d "$subdir" ]; then
        echo "Directory '$subdir' does not exist. Skipping."
        continue
    fi

    echo "Processing directory: $subdir"

    # Create the output directory "anim" within this subdirectory
    anim_dir="$subdir/anim"
    mkdir -p "$anim_dir"

    # Loop over all PNG files in the subdirectory
    for png in "$subdir"/*.png; do
        # Check if any PNG file exists; if not, skip
        if [ ! -f "$png" ]; then
            echo "No PNG files found in $subdir."
            break
        fi

        # Extract the base name (e.g., 'image' from 'image.png')
        base=$(basename "$png" .png)
        output_file="$anim_dir/${base}.mp4"
        echo "Processing '$png' -> '$output_file'"

        # Run the Python animation script (adjust path if necessary)
        python slot_animation.py --input "$png" --output "$output_file"
    done
done
