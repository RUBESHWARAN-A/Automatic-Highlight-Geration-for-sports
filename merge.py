import os
from moviepy.editor import VideoFileClip, concatenate_videoclips

def merge_highlight_clips(folder_path, output_file):
    # Get a list of all video files in the specified folder
    files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.mp4')]

    # Create VideoFileClip objects for each video file
    clips = [VideoFileClip(file) for file in files]

    # Concatenate the video clips
    final_clip = concatenate_videoclips(clips)

    # Write the concatenated highlight clip to a file
    final_clip.write_videofile(output_file)

    # Print a message indicating completion
    print(f"Highlight clips merged successfully into {output_file}")

# Example usage
merge_highlight_clips('Subclips', 'highlights_merged.mp4')
