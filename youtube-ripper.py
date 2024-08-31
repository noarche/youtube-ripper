import yt_dlp
import os
from termcolor import colored
import sys

apikey='''                                                       
[91m@[0m[93m@[0m[92m@[0m[96m@[0m[94m@[0m[95m@[0m[91m@[0m   [93m@[0m[92m@[0m[96m@[0m  [94m@[0m[95m@[0m[91m@[0m[93m@[0m[92m@[0m[96m@[0m[94m@[0m   [95m@[0m[91m@[0m[93m@[0m[92m@[0m[96m@[0m[94m@[0m[95m@[0m   [91m@[0m[93m@[0m[92m@[0m[96m@[0m[94m@[0m[95m@[0m[91m@[0m[93m@[0m  [92m@[0m[96m@[0m[94m@[0m[95m@[0m[91m@[0m[93m@[0m[92m@[0m   
[96m@[0m[94m@[0m[95m@[0m[91m@[0m[93m@[0m[92m@[0m[96m@[0m[94m@[0m  [95m@[0m[91m@[0m[93m@[0m  [92m@[0m[96m@[0m[94m@[0m[95m@[0m[91m@[0m[93m@[0m[92m@[0m[96m@[0m  [94m@[0m[95m@[0m[91m@[0m[93m@[0m[92m@[0m[96m@[0m[94m@[0m[95m@[0m  [91m@[0m[93m@[0m[92m@[0m[96m@[0m[94m@[0m[95m@[0m[91m@[0m[93m@[0m  [92m@[0m[96m@[0m[94m@[0m[95m@[0m[91m@[0m[93m@[0m[92m@[0m[96m@[0m  
[94m@[0m[95m@[0m[91m![0m  [93m@[0m[92m@[0m[96m@[0m  [94m@[0m[95m@[0m[91m![0m  [93m@[0m[92m@[0m[96m![0m  [94m@[0m[95m@[0m[91m@[0m  [93m@[0m[92m@[0m[96m![0m  [94m@[0m[95m@[0m[91m@[0m  [93m@[0m[92m@[0m[96m![0m       [94m@[0m[95m@[0m[91m![0m  [93m@[0m[92m@[0m[96m@[0m  
[94m![0m[95m@[0m[91m![0m  [93m@[0m[92m![0m[96m@[0m  [94m![0m[95m@[0m[91m![0m  [93m![0m[92m@[0m[96m![0m  [94m@[0m[95m![0m[91m@[0m  [93m![0m[92m@[0m[96m![0m  [94m@[0m[95m![0m[91m@[0m  [93m![0m[92m@[0m[96m![0m       [94m![0m[95m@[0m[91m![0m  [93m@[0m[92m![0m[96m@[0m  
[94m@[0m[95m![0m[91m@[0m[93m![0m[92m![0m[96m@[0m[94m![0m   [95m![0m[91m![0m[93m@[0m  [92m@[0m[96m![0m[94m@[0m[95m@[0m[91m![0m[93m@[0m[92m![0m   [96m@[0m[94m![0m[95m@[0m[91m@[0m[93m![0m[92m@[0m[96m![0m   [94m@[0m[95m![0m[91m![0m[93m![0m[92m:[0m[96m![0m    [94m@[0m[95m![0m[91m@[0m[93m![0m[92m![0m[96m@[0m[94m![0m   
[95m![0m[91m![0m[93m@[0m[92m![0m[96m@[0m[94m![0m    [95m![0m[91m![0m[93m![0m  [92m![0m[96m![0m[94m@[0m[95m![0m[91m![0m[93m![0m    [92m![0m[96m![0m[94m@[0m[95m![0m[91m![0m[93m![0m    [92m![0m[96m![0m[94m![0m[95m![0m[91m![0m[93m:[0m    [92m![0m[96m![0m[94m@[0m[95m![0m[91m@[0m[93m![0m    
[92m![0m[96m![0m[94m:[0m [95m:[0m[91m![0m[93m![0m   [92m![0m[96m![0m[94m:[0m  [95m![0m[91m![0m[93m:[0m       [92m![0m[96m![0m[94m:[0m       [95m![0m[91m![0m[93m:[0m       [92m![0m[96m![0m[94m:[0m [95m:[0m[91m![0m[93m![0m   
[92m:[0m[96m![0m[94m:[0m  [95m![0m[91m:[0m[93m![0m  [92m:[0m[96m![0m[94m:[0m  [95m:[0m[91m![0m[93m:[0m       [92m:[0m[96m![0m[94m:[0m       [95m:[0m[91m![0m[93m:[0m       [92m:[0m[96m![0m[94m:[0m  [95m![0m[91m:[0m[93m![0m  
[92m:[0m[96m:[0m   [94m:[0m[95m:[0m[91m:[0m   [93m:[0m[92m:[0m   [96m:[0m[94m:[0m        [95m:[0m[91m:[0m        [93m:[0m[92m:[0m [96m:[0m[94m:[0m[95m:[0m[91m:[0m  [93m:[0m[92m:[0m   [96m:[0m[94m:[0m[95m:[0m  
 [91m:[0m   [93m:[0m [92m:[0m  [96m:[0m     [94m:[0m         [95m:[0m        [91m:[0m [93m:[0m[92m:[0m [96m:[0m[94m:[0m    [95m:[0m   [91m:[0m [93m:[0m  
                                                       
'''



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
        total_bytes = d.get('total_bytes', 0)
        total_size_mb = round(total_bytes / 1024 / 1024, 2) if total_bytes else 'Unknown'
        sys.stdout.write(f"\r{colored('Downloading:', 'cyan', attrs=['bold'])} {p} at {speed} (ETA: {eta}, Size: {total_size_mb} MB)")
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
    ydl_opts['noplaylist'] = not is_playlist

    # Download the media
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

print(apikey)

def main():
    while True:
        # Display the menu
        cprint("[91mA[0m[93mn[0m[92my[0m [96mW[0m[94me[0m[95mb[0m[91ms[0m[93mi[0m[92mt[0m[96me[0m [94m|[0m [95mH[0m[91mi[0m[93mg[0m[92mh[0m[96me[0m[94ms[0m[95mt[0m [91mQ[0m[93mu[0m[92ma[0m[96ml[0m[94mi[0m[95mt[0m[91my[0m [93mb[0m[92my[0m [96mD[0m[94me[0m[95mf[0m[91ma[0m[93mu[0m[92ml[0m[96mt[0m [94m|[0m [95mV[0m[91mi[0m[93md[0m[92me[0m[96mo[0m [94mD[0m[95mo[0m[91mw[0m[93mn[0m[92ml[0m[96mo[0m[94ma[0m[95md[0m[91me[0m[93mr[0m [92m|[0m [96mA[0m[94mu[0m[95md[0m[91mi[0m[93mo[0m [92mD[0m[96mo[0m[94mw[0m[95mn[0m[91ml[0m[93mo[0m[92ma[0m[96md[0m[94me[0m[95mr[0m")
        cprint("https://github.com/noarche/youtube-ripper", color='blue')
        cprint("Make a selection for audio or video & playlist. Leave options blank for quick default setting.", color='magenta')
        cprint("Enter the link and wait until prompted for another link!!", color='red')
        cprint("The same settings will be used for the next link unless you return to the menu.", color='red')
        cprint("Return to the menu to start over by typing 'm' or 'menu' instead of another link.", color='yellow')
        cprint("\n", color='blue')
        cprint("1: Download Video", color='green')
        cprint("2: Download Audio", color='green')

        choice = input(colored("Enter your choice (1-2): ", 'cyan', attrs=['bold'])).strip() or '1'
        is_playlist_input = input(colored("Is this a playlist? (y/n): ", 'cyan', attrs=['bold'])).strip().lower()
        is_playlist = is_playlist_input == 'y' if is_playlist_input else False
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
