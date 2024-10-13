import os
import sys
from pytube import Search, YouTube
from moviepy.editor import AudioFileClip
from pydub import AudioSegment

def download_videos(singer_name, num_videos):
    search = Search(singer_name)
    search_results = search.results[:num_videos]
    video_urls = [video.watch_url for video in search_results]

    video_files = []
    for idx, url in enumerate(video_urls):
        yt = YouTube(url)
        video = yt.streams.filter(only_audio=True).first()
        print(f"Downloading video {idx+1}: {yt.title}")
        out_file = video.download(output_path="videos")
        video_files.append(out_file)
    
    return video_files

def process_audio(video_files, audio_duration):
    audio_clips = []
    for idx, video in enumerate(video_files):
        # Convert video to audio
        audio = AudioFileClip(video)
        # Cut the first Y seconds
        audio = audio.subclip(0, audio_duration)
        # Save each audio clip
        audio_file = f"audio_{idx+1}.mp3"
        audio.write_audiofile(audio_file)
        audio_clips.append(audio_file)
    
    return audio_clips

def merge_audios(audio_files, output_file):
    combined_audio = None
    for idx, audio_file in enumerate(audio_files):
        current_audio = AudioSegment.from_file(audio_file)
        # Append or start the merged audio
        if combined_audio is None:
            combined_audio = current_audio
        else:
            combined_audio += current_audio
    
    combined_audio.export(output_file, format="mp3")
    print(f"Merged audio saved as {output_file}")

def main():
    if len(sys.argv) != 5:
        print("Usage: python <program.py> <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>")
        sys.exit(1)
    
    try:
        singer_name = sys.argv[1]
        num_videos = int(sys.argv[2])
        audio_duration = int(sys.argv[3])
        output_file = sys.argv[4]

        if num_videos < 10 or audio_duration <= 20:
            print("Number of videos must be greater than 10 and audio duration must be greater than 20 seconds.")
            sys.exit(1)

        if not os.path.exists("videos"):
            os.makedirs("videos")

        video_files = download_videos(singer_name, num_videos)

        audio_files = process_audio(video_files, audio_duration)

        merge_audios(audio_files, output_file)

        for file in video_files + audio_files:
            os.remove(file)

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
