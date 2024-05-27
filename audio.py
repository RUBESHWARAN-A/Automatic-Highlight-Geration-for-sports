import os
import moviepy.editor as mp

def generate_audio(video_path):
    # Load the video clip
    video_clip = mp.VideoFileClip(video_path)
    
    # Extract audio from the video clip
    audio_clip = video_clip.audio
    
    # Set the path for saving the audio file
    audio_filename = os.path.splitext(os.path.basename(video_path))[0] + '.wav'
    audio_path = os.path.join(os.path.dirname(video_path), audio_filename)
    
    # Write the audio clip to a WAV file
    audio_clip.write_audiofile(audio_path)
    
    return audio_path

# Example usage
video_path = 'video.mp4'
audio_path = generate_audio(video_path)

