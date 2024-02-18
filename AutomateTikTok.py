#GOAL: Automate those low effort TikToks that have TTS over parkour or TV,
import praw
from main import tts
import pydub
import os
import glob
import moviepy
from moviepy.editor import *
from moviepy.config import change_settings
import random 
change_settings({"IMAGEMAGICK_BINARY": "/opt/homebrew/Cellar/imagemagick/7.1.1-24/bin/convert"}) # Fixed imageMagick error
import whisper_timestamped
import re
import subprocess
from mutagen.mp3 import MP3
import elevenlabs
import requests
# Reddit API, this is the first step, web scraping 
secret = 'e6Ges3MV7gJKGMwIWQeM7oNbLgH2Eg'
client_id = 'jUbb6_7qhELN-KR2VESchQ'
client_user = 'Medium-Tourist3232'
user_agent = 'MacOS:Med-Tourist:1.0 (by u/Medium-Tourist3232)'
password = 'gabe1234'

reddit = praw.Reddit(
    client_id= client_id,
    client_secret= secret,
    password= password,
    user_agent= user_agent,
    username=client_user,
)



def AITAHdata(submission_limit): # Webscrapes the data from reddit
    subreddit = reddit.subreddit('AITAH')

    post_titles = []
    Post_bodies = []
    for submission in subreddit.top(time_filter = 'week', limit = submission_limit): 
        post_title = submission.title
        post_titles.append(post_title)
        post_body = submission.selftext
        Post_bodies.append(post_body)
   
    with open('/Users/gabemeredith/Code/python /tiktok-voice-main/AutomatingTIkToks/Titles.txt','w') as file:
        for item in post_titles:
            file.write(item + '\n')
       
    with open('/Users/gabemeredith/Code/python /tiktok-voice-main/AutomatingTIkToks/comments.txt','w') as file:
        for item in Post_bodies:
            file.write(item + '\n')
            

# Use for ASkreddit 
def iterateinfo(submission_limit,comment_limit):
    subreddit = reddit.subreddit('AskReddit')

    post_titles = []
    top_comments = []
    for submission in subreddit.hot(time_filter = 'day', limit = submission_limit):
        post_title = submission.title
        post_titles.append(post_title)
        submission.comment_sort = "top"
        submission.comment_limit = comment_limit
        submission.comments.replace_more(limit=0)
        comments = submission.comments
        for comment in comments:
            comment_word = comment.body
            top_comments.append(comment_word)
    file = open('/Users/gabemeredith/Code/python /tiktok-voice-main/AutomatingTIkToks/Titles.txt','w') # could use 'with', but not sure if it will work
    for item in post_titles:
        try:
            file.write(item + '\n')
        finally:  
            file.close()
    file = open('/Users/gabemeredith/Code/python /tiktok-voice-main/AutomatingTIkToks/comments.txt','w')
    for item in top_comments:
        try: 
            file.write(item + '\n')
        finally:
            file.close()
            
file_titles = open('/Users/gabemeredith/Code/python /tiktok-voice-main/AutomatingTIkToks/Titles.txt','r', errors='ignore', encoding='utf-8').read() 
file_comments = open('/Users/gabemeredith/Code/python /tiktok-voice-main/AutomatingTIkToks/filteredcomment.txt', 'r', errors='ignore', encoding='utf-8').read()

def remove_double(): # have to use on AITAH 
    file_path = '/Users/gabemeredith/Code/python /tiktok-voice-main/AutomatingTIkToks/comments.txt'
    
    # Open the file in read mode and read the content
    with open(file_path, 'r') as file:
        content = file.read()

    # Replace double line breaks with single ones
    content = content.replace('\n\n', '\n')

    # Open the file in write mode and write the modified content
    with open(file_path, 'w') as file:
        file.write(content)

# def filter_for_length():
#     input_file_path = '/Users/gabemeredith/Code/python /tiktok-voice-main/AutomatingTIkToks/filteredcomment.txt'
#     output_file_path = '/Users/gabemeredith/Code/python /tiktok-voice-main/AutomatingTIkToks/readyfortts.txt'

#     with open(input_file_path, 'r') as file, open(output_file_path, 'w') as output_file:
#         for line in file:
#             # Remove leading and trailing whitespace
#             line = line.strip()

#             # Split the line into chunks of 200 characters
#             for i in range(0, len(line), 200):
#                 chunk = line[i:i+200]
#                 output_file.write(chunk + '\n')
def filter_for_length():
    input_file_path = '/Users/gabemeredith/Code/python /tiktok-voice-main/AutomatingTIkToks/filteredcomment.txt'
    output_file_path = '/Users/gabemeredith/Code/python /tiktok-voice-main/AutomatingTIkToks/readyfortts.txt'

    with open(input_file_path, 'r') as file, open(output_file_path, 'w') as output_file:
        for line in file:
            line = line.strip()
            while len(line) > 0:
                # Find the nearest space before the 200-character limit
                split_index = min(len(line), 200)
                if len(line) > 200:
                    split_index = line.rfind(' ', 0, 200)

                # If no space is found, just use the 200-character limit
                if split_index == -1:
                    split_index = 200

                chunk = line[:split_index].strip()
                output_file.write(chunk + '\n')

                # Remove the processed chunk from the line
                line = line[split_index:].strip()

def filter_for_punc():
    pattern = r'https?://\S+|\u200B'
    filtered_comments = []
    with open('/Users/gabemeredith/Code/python /tiktok-voice-main/AutomatingTIkToks/comments.txt', 'r') as file:
        for line in file:
            clean_comment = re.sub(pattern, '', line) # only use line.strip if AITAH
            filtered_comments.append(clean_comment)

    with open('/Users/gabemeredith/Code/python /tiktok-voice-main/AutomatingTIkToks/comments.txt', 'w') as file:
        for comment in filtered_comments:
            file.write(comment)
    # So basically Im kinda lazy so like IF using ASKREDDIT USE THIS ONE UNDER
    #open('/Users/gabemeredith/Code/python /tiktok-voice-main/AutomatingTIkToks/filteredcomment.txt','w').writelines(line for line in open('/Users/gabemeredith/Code/python /tiktok-voice-main/AutomatingTIkToks/comments.txt') if 150 < len(line) < 200)
    # IF using AITAH use this one!!
    open('/Users/gabemeredith/Code/python /tiktok-voice-main/AutomatingTIkToks/filteredcomment.txt','w').writelines(line for line in open('/Users/gabemeredith/Code/python /tiktok-voice-main/AutomatingTIkToks/comments.txt'))


def AITA_replace_jargon():
   # Read the file
    file_path = '/Users/gabemeredith/Code/python /tiktok-voice-main/AutomatingTIkToks/readyfortts.txt'
    with open(file_path, 'r') as file:
        content = file.read()

    # Replace 'AITA' with the new phrase
    content = content.replace('AITAH', 'Am I the Asshole')
    content = content.replace('AITA', 'Am I the Asshole')

    # Replace patterns like '23F' or '45M' with '23 Female' or '45 Male'
    content = re.sub(r'(\d+)\s*(f|m)', lambda x: f"{x.group(1)} {'Female' if x.group(2).lower() == 'f' else 'Male'}", content, flags=re.IGNORECASE)


    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.write(content)
        
        
    file_path2 = '/Users/gabemeredith/Code/python /tiktok-voice-main/AutomatingTIkToks/Titles.txt'
    
    with open(file_path2, 'r') as file:
        content = file.read()

    # Replace 'AITA' with the new phrase
    content = content.replace('AITAH', 'Am I the Asshole')
    content = content.replace('AITA', 'Am I the Asshole')

    # Replace patterns like '23F' or '45M' with '23 Female' or '45 Male'
    content = re.sub(r'(\d+)\s*(f|m)',lambda x: f"{x.group(1)} {'Female' if x.group(2).lower() == 'f' else 'Male'}", content, flags=re.IGNORECASE)


    # Write the modified content back to the file
    with open(file_path2, 'w') as file:
        file.write(content)
        
def tts_on_title():  
    with open('/Users/gabemeredith/Code/python /tiktok-voice-main/AutomatingTIkToks/Titles.txt', 'r', errors='ignore', encoding='utf-8') as file:
        for line_number, line in enumerate(file, start=0):
            file_out_name = f"/Users/gabemeredith/Code/python /tiktok-voice-main/TTS/non-combined/title{line_number}.mp3"
            tts(session_id='3a7cca57c0e729bfa4e40a5615de3765', text_speaker='en_us_006', req_text=line.strip(), filename=file_out_name, play=False)


# def text_to_speech_elevenlabs():
#     # Read text from the file
#     try:
#         with open('/Users/gabemeredith/Code/python /tiktok-voice-main/AutomatingTIkToks/combined.txt', 'r') as file:
#             text = file.read()
#     except FileNotFoundError:
#         return "File not found."
#     api_key = "c7a77a571798f38979434f83a3e400cd"

#     # Set up the API endpoint and headers
#     url = "https://api.elevenlabs.io/speech"
#     headers = {
#         'Authorization': f'Bearer {api_key}',
#         'Content-Type': 'application/json'
#     }

#     # Set up the data payload
#     data = {
#         "text": text,
#         "voice": "premade/Adam"
#     }

#     # Make the request to ElevenLabs API
#     response = requests.post(url, json=data, headers=headers)

#     if response.status_code == 200:
#         # Assuming the API returns a URL to the audio file
#         audio_url = response.json().get('audioUrl')
#         return audio_url
#     else:
#         return "Error in text-to-speech conversion."

    
def tts_on_multi():
    # Use 'with' statement for better handling of file opening/closing
    with open('/Users/gabemeredith/Code/python /tiktok-voice-main/AutomatingTIkToks/readyfortts.txt', 'r', errors='ignore', encoding='utf-8') as file:
        for line_number, line in enumerate(file, start=0):
            file_out_name = f"/Users/gabemeredith/Code/python /tiktok-voice-main/TTS/non-combined/comments{line_number}.mp3"
            tts(session_id='3a7cca57c0e729bfa4e40a5615de3765', text_speaker='en_us_006', req_text=line.strip(), filename=file_out_name, play=False)

def combine_mp3s():
    directory = '/Users/gabemeredith/Code/python /tiktok-voice-main/TTS/non-combined'
    mp3_files = [f for f in os.listdir(directory) if f.endswith('.mp3')]
    
    def extract_number(file_name):
        match = re.search(r'comments(\d+)', file_name)
        return int(match.group(1)) if match else float('inf')

    # Sort the files numerically based on the line number
    mp3_files.sort(key=extract_number)

    # Sort the files so that the title comes first
    mp3_files.sort(key=lambda x: 'title' not in x)  # Replace 'title' with the identifiable part of your title file's name

    sounds = [pydub.AudioSegment.from_mp3(os.path.join(directory, mp3_file)) for mp3_file in mp3_files]
    combined = pydub.AudioSegment.empty()

    for sound in sounds:
        combined += sound
    combined.export("/Users/gabemeredith/Code/python /tiktok-voice-main/TTS/Completed/Combined.mp3", format="mp3")
    
    
    
def clean_dir():
    files = glob.glob('/Users/gabemeredith/Code/python /tiktok-voice-main/TTS/non-combined/*.mp3')
    for f in files:
        os.remove(f)
        
        
# Function to read a file and split into words
def create_combine():
    
    def read_and_split(file_path):
        with open(file_path, 'r') as file:
            text = file.read()
            words = text.split()
        return words

# Read and split both files
    words_file1 = read_and_split('/Users/gabemeredith/Code/python /tiktok-voice-main/AutomatingTIkToks/Titles.txt')
    words_file2 = read_and_split('/Users/gabemeredith/Code/python /tiktok-voice-main/AutomatingTIkToks/readyfortts.txt')

# Combine the words from both files
    combined_words = []
    for word1 in words_file1:
        combined_words.append(word1)
    for word2 in words_file2:
        combined_words.append(word2)
        

# Write the combined words to a new file
    with open('/Users/gabemeredith/Code/python /tiktok-voice-main/AutomatingTIkToks/combined.txt', 'w') as combined_file:
        combined_file.write(' '.join(combined_words))

# Actually, Imma try whisper to see if it's better
    
def Create_sub():
    model = whisper_timestamped.load_model('medium') # biggest thing is changing models and test it, maybe on PC? 
    audio = '/Users/gabemeredith/Code/python /tiktok-voice-main/TTS/Completed/Combined.mp3'
    results = whisper_timestamped.transcribe(model,audio)
    New_gameplay = VideoFileClip('/Users/gabemeredith/Code/python /tiktok-voice-main/AutomatingTIkToks/60Sgameplay.mp4')
    subs = []
    subs.append(New_gameplay)
    for segment in results['segments']:
         for word in segment["words"]:
             text = word['text'].upper()
             start = word['start']
             end = word['end']
             duration = end - start
             txt_clip = TextClip(txt = text, fontsize=60,font = 'Comic-Sans-MS-Bold',method = 'caption', color= 'white',stroke_color='black').set_position('center')
             txt_clip = txt_clip.set_start(start).set_duration(duration).set_pos(('center','center'))
             subs.append(txt_clip)  # Append each txt_clip to subs

     #Create a composite video clip with all the text clips
    clip = CompositeVideoClip(subs)
    clip.write_videofile("/Users/gabemeredith/Code/python /tiktok-voice-main/AutomatingTIkToks/Video_file.mp4", fps=25, codec='libx264')

def create_audio_on_subs():
    audioclip = AudioFileClip("/Users/gabemeredith/Code/python /tiktok-voice-main/TTS/Completed/Combined.mp3")
    clip = VideoFileClip('/Users/gabemeredith/Code/python /tiktok-voice-main/AutomatingTIkToks/Video_file.mp4', audio= True)     
    clip = clip.set_audio(audioclip)
    clip.write_videofile("/Users/gabemeredith/Code/python /tiktok-voice-main/AutomatingTIkToks/finished.mp4", fps=25, codec='libx264')
    
    
def reencode_video():
    """
    Re-encodes the audio of the video file using FFmpeg.

    Args:
    input_file (str): Path to the input video file.
    output_file (str): Path where the output video file will be saved.
    """
    input_file = '/Users/gabemeredith/Code/python /tiktok-voice-main/AutomatingTIkToks/finished.mp4'
    output_file = '/Users/gabemeredith/Code/python /tiktok-voice-main/AutomatingTIkToks/Video_file/ready.mp4'
    try:
        command = [
            'ffmpeg', 
            '-i', input_file, 
            '-c:v', 'copy',    # Copy the video as is
            '-c:a', 'aac',     # Re-encode audio to AAC
            '-strict', '-2',   # Some versions of FFmpeg require '-strict -2' for AAC
            output_file
        ]
        subprocess.run(command, check=True)
        print(f"Video re-encoded successfully: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

 
def automate_audio():
    clean_dir()
    #iterateinfo(1,3) #use for askreddit
    AITAHdata(1) # AITAH
    remove_double()
    filter_for_punc()
    filter_for_length()
    AITA_replace_jargon()
    tts_on_title()
    create_combine()
    tts_on_multi()
    combine_mp3s()
    clean_dir()
    
    
    
    ### Visual time
path_to_script = '/Users/gabemeredith/Code/python /tiktok-voice-main/AutomatingTIkToks/combined.txt'



def make_vid():
    file_path = "/Users/gabemeredith/Code/python /tiktok-voice-main/TTS/Completed/Combined.mp3" 
    audio = MP3(file_path)
    duration = audio.info.length
    gameplay = VideoFileClip("/Users/gabemeredith/Downloads/13 Minutes Minecraft Parkour Gameplay [Free to Use] [Map Download].mp4", audio = False)
    max_start = max(0, gameplay.duration - duration)
    start_time = random.uniform(0, max_start)
    new_clip = gameplay.subclip(start_time, start_time + duration)

    # Save the new clip
    output_path = '/Users/gabemeredith/Code/python /tiktok-voice-main/AutomatingTIkToks/60Sgameplay.mp4'
    new_clip.write_videofile(output_path, codec='libx264')

    
    
    
def main():
    automate_audio()
    make_vid()
    Create_sub()
    create_audio_on_subs()
    reencode_video()
    
    
        #tts(session_id='13dc2c6357484a029686688de60a5f1c8',text_speaker='en_us_006',req_text=file_comments,filename='/Users/gabemeredith/Code/python /tiktok-voice-main/TTS/comments.mp3',play=False)
        
if __name__ == '__main__':
    main()
   
    
# python -u "/Users/gabemeredith/Code/python /tiktok-voice-main/main.py" -v 'en_us_006' -f '/Users/gabemeredith/Code/python /tiktok-voice-main/AutomatingTIkToks/comments.txt' -n '/Users/gabemeredith/Code/python /tiktok-voice-main/TTS/test.mp3' --session '13dc2c6357484a029686688e60a5f1c8'
# python -u "/Users/gabemeredith/Code/python /tiktok-voice-main/main.py" -v 'en_us_006' -f '/Users/gabemeredith/Code/python /tiktok-voice-main/AutomatingTIkToks/titles.txt' -n '/Users/gabemeredith/Code/python /tiktok-voice-main/TTS/test.mp3' --session '13dc2c6357484a029686688e60a5f1c8'

# Google ACCOUND redditlongbottom@gmail.com PW : ChristainBalestan123