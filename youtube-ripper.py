import yt_dlp
import os
from termcolor import colored
import sys

# Ensure download directories exist
os.makedirs('./downloads-audio', exist_ok=True)
os.makedirs('./downloads-video', exist_ok=True)

# Function to print with colors
def cprint(text, color='blue', attrs=['bold']):
    print(colored(text, color, attrs=attrs))

# Progress bar hook function
def progress_hook(d):
    if d['status'] == 'downloading':
        p = d['_percent_str']
        speed = d['_speed_str']
        eta = d['_eta_str']
        sys.stdout.write(f"\r{colored('Downloading:', 'cyan', attrs=['bold'])} {p} at {speed} (ETA: {eta})")
        sys.stdout.flush()
    elif d['status'] == 'finished':
        sys.stdout.write(f"\r{colored('Download completed!', 'green', attrs=['bold'])}                  \n")
        sys.stdout.flush()

def download_media(url, download_type='video', is_playlist=False):
    # Configure options based on user input
    ydl_opts = {
        'progress_hooks': [progress_hook],
    }

    if download_type == 'video':
        ydl_opts.update({
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': './downloads-video/%(title)s.%(ext)s',  # Save videos in downloads-video folder
        })
    elif download_type == 'audio':
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': './downloads-audio/%(title)s.%(ext)s',  # Save audios in downloads-audio folder
        })

    # Adjust noplaylist option based on is_playlist
    if is_playlist:
        ydl_opts['noplaylist'] = False
    else:
        ydl_opts['noplaylist'] = True

    # Download the media
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def main():
    while True:
        # Display the menu
        cprint("YouTube-Ripper", color='magenta')
        cprint("https://github.com/noarche/youtube-ripper", color='white')
        cprint("Make a selection for audio or video.", color='blue')
        cprint("Select if it is a playlist or single item.", color='blue')
        cprint("Enter the link and wait until prompted for another link.", color='blue')
        cprint("The same settings will be used for the next link unless you return to the menu.", color='blue')
        cprint("Return to the menu to start over by typing 'm' or 'menu' instead of another link.", color='blue')
        cprint("\n", color='blue')
        cprint("1: Download Video", color='yellow')
        cprint("2: Download Audio", color='yellow')

        choice = input(colored("Enter your choice (1-2): ", 'cyan', attrs=['bold']))

        if choice not in ['1', '2']:
            cprint("Invalid choice! Please select a number between 1 and 2.", color='red')
            continue

        is_playlist = input(colored("Is this a playlist? (y/n): ", 'cyan', attrs=['bold'])).lower() == 'y'
        download_type = 'video' if choice == '1' else 'audio'

        while True:
            url = input(colored("Enter the YouTube URL (type 'menu'/'m' to return to the menu, 'exit'/'e' to exit): ", 'cyan', attrs=['bold'])).strip()

            if url.lower() in ['exit', 'e']:
                cprint("Exiting...", color='red')
                return
            elif url.lower() in ['menu', 'm']:
                break  # Go back to the main menu
            else:
                download_media(url, download_type=download_type, is_playlist=is_playlist)
                cprint(f"{download_type.capitalize()} download completed!", color='green')

if __name__ == "__main__":
    main()
