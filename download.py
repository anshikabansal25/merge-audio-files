import yt_dlp
import os
from pydub import AudioSegment
import zipfile

# Step 1: Download videos from YouTube
# Set the search term
search_query = "sheery mann songs"

# Create a new folder for the downloaded videos
output_folder = "SheeryMannSongs"
os.makedirs(output_folder, exist_ok=True)

# Options for downloading videos
ydl_opts = {
    'format': '136+140',  # Select the 720p video and medium quality audio
    'noplaylist': True,    # Avoid downloading entire playlists
    'quiet': False,
    'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
    'merge_output_format': 'mp4'  # Ensure the output is combined into mp4
}





print(f"Downloaded the first 5 videos into the folder: {output_folder}")

# Step 2: Extract and process audio from the downloaded videos
# Define the folder containing video files
video_folder = os.path.abspath(output_folder)  # Absolute path for consistency
audio_folder = os.path.join(os.path.dirname(video_folder), "audios")

os.makedirs(audio_folder, exist_ok=True)

# List all video files in the video folder
video_files = [f for f in os.listdir(video_folder) if f.endswith(('.mp4', '.mkv', '.avi', '.mov'))]

# Process each video file
for video_file in video_files:
    video_file_path = os.path.join(video_folder, video_file)
    audio_file_path = os.path.join(audio_folder, f"{os.path.splitext(video_file)[0]}.wav")

    # Extract audio using pydub
    video_audio = AudioSegment.from_file(video_file_path)

    # Skip the first 30 seconds of the audio
    start_time = 30 * 1000  # pydub works in milliseconds
    trimmed_audio = video_audio[start_time:]

    # Export the trimmed audio
    trimmed_audio.export(audio_file_path, format="wav")

    print(f"Extracted audio from {video_file} to {audio_file_path} (skipping first 30 seconds)")

print("Audio extraction complete for all videos.")

# Step 3: Merge the extracted audio files
audio_files = [f for f in os.listdir(audio_folder) if f.endswith('.wav')]

# Concatenate audio clips using pydub
if audio_files:  # Check if there are audio clips
    combined_audio = AudioSegment.empty()
    
    for audio_file in audio_files:
        audio_path = os.path.join(audio_folder, audio_file)
        audio_segment = AudioSegment.from_wav(audio_path)
        combined_audio += audio_segment  # Append audio segments

    # Define the output path for the merged audio
    merged_audio_path = os.path.join(audio_folder, "merged_audio.wav")

    # Export the merged audio
    combined_audio.export(merged_audio_path, format="wav")

    print(f"Merged audio saved to {merged_audio_path}")

    # Step 4: Zip the merged audio file
    # Define the path to the file you want to zip
    file_to_zip = merged_audio_path

    # Define the path for the zip file
    zip_file_path = os.path.join(audio_folder, "merged_audio.zip")

    # Create a Zip file and add the file to it
    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        # Add the file to the zip file
        zipf.write(file_to_zip, os.path.basename(file_to_zip))

    print(f"The file {file_to_zip} has been zipped into {zip_file_path}")

else:
    print("No audio files were found to merge.")
