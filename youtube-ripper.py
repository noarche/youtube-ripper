import yt_dlp
import os
from termcolor import colored
import sys
import signal

main_logo = '''
   [91m▄[0m[93m█[0m[92m█[0m[96m█[0m[94m█[0m[95m█[0m[91m█[0m[93m█[0m[92m█[0m  [96m▄[0m[94m█[0m     [95m▄[0m[91m█[0m[93m█[0m[92m█[0m[96m█[0m[94m█[0m[95m█[0m[91m█[0m[93m▄[0m    [92m▄[0m[96m█[0m[94m█[0m[95m█[0m[91m█[0m[93m█[0m[92m█[0m[96m█[0m[94m▄[0m    [95m▄[0m[91m█[0m[93m█[0m[92m█[0m[96m█[0m[94m█[0m[95m█[0m[91m█[0m[93m█[0m    [92m▄[0m[96m█[0m[94m█[0m[95m█[0m[91m█[0m[93m█[0m[92m█[0m[96m█[0m[94m█[0m 
  [95m█[0m[91m█[0m[93m█[0m    [92m█[0m[96m█[0m[94m█[0m [95m█[0m[91m█[0m[93m█[0m    [92m█[0m[96m█[0m[94m█[0m    [95m█[0m[91m█[0m[93m█[0m   [92m█[0m[96m█[0m[94m█[0m    [95m█[0m[91m█[0m[93m█[0m   [92m█[0m[96m█[0m[94m█[0m    [95m█[0m[91m█[0m[93m█[0m   [92m█[0m[96m█[0m[94m█[0m    [95m█[0m[91m█[0m[93m█[0m 
  [92m█[0m[96m█[0m[94m█[0m    [95m█[0m[91m█[0m[93m█[0m [92m█[0m[96m█[0m[94m█[0m[95m▌[0m   [91m█[0m[93m█[0m[92m█[0m    [96m█[0m[94m█[0m[95m█[0m   [91m█[0m[93m█[0m[92m█[0m    [96m█[0m[94m█[0m[95m█[0m   [91m█[0m[93m█[0m[92m█[0m    [96m█[0m[94m▀[0m    [95m█[0m[91m█[0m[93m█[0m    [92m█[0m[96m█[0m[94m█[0m 
 [95m▄[0m[91m█[0m[93m█[0m[92m█[0m[96m▄[0m[94m▄[0m[95m▄[0m[91m▄[0m[93m█[0m[92m█[0m[96m▀[0m [94m█[0m[95m█[0m[91m█[0m[93m▌[0m   [92m█[0m[96m█[0m[94m█[0m    [95m█[0m[91m█[0m[93m█[0m   [92m█[0m[96m█[0m[94m█[0m    [95m█[0m[91m█[0m[93m█[0m  [92m▄[0m[96m█[0m[94m█[0m[95m█[0m[91m▄[0m[93m▄[0m[92m▄[0m      [96m▄[0m[94m█[0m[95m█[0m[91m█[0m[93m▄[0m[92m▄[0m[96m▄[0m[94m▄[0m[95m█[0m[91m█[0m[93m▀[0m 
[92m▀[0m[96m▀[0m[94m█[0m[95m█[0m[91m█[0m[93m▀[0m[92m▀[0m[96m▀[0m[94m▀[0m[95m▀[0m   [91m█[0m[93m█[0m[92m█[0m[96m▌[0m [94m▀[0m[95m█[0m[91m█[0m[93m█[0m[92m█[0m[96m█[0m[94m█[0m[95m█[0m[91m█[0m[93m█[0m[92m▀[0m  [96m▀[0m[94m█[0m[95m█[0m[91m█[0m[93m█[0m[92m█[0m[96m█[0m[94m█[0m[95m█[0m[91m█[0m[93m▀[0m  [92m▀[0m[96m▀[0m[94m█[0m[95m█[0m[91m█[0m[93m▀[0m[92m▀[0m[96m▀[0m     [94m▀[0m[95m▀[0m[91m█[0m[93m█[0m[92m█[0m[96m▀[0m[94m▀[0m[95m▀[0m[91m▀[0m[93m▀[0m   
[92m▀[0m[96m█[0m[94m█[0m[95m█[0m[91m█[0m[93m█[0m[92m█[0m[96m█[0m[94m█[0m[95m█[0m[91m█[0m[93m█[0m [92m█[0m[96m█[0m[94m█[0m    [95m█[0m[91m█[0m[93m█[0m          [92m█[0m[96m█[0m[94m█[0m          [95m█[0m[91m█[0m[93m█[0m    [92m█[0m[96m▄[0m  [94m▀[0m[95m█[0m[91m█[0m[93m█[0m[92m█[0m[96m█[0m[94m█[0m[95m█[0m[91m█[0m[93m█[0m[92m█[0m[96m█[0m 
  [94m█[0m[95m█[0m[91m█[0m    [93m█[0m[92m█[0m[96m█[0m [94m█[0m[95m█[0m[91m█[0m    [93m█[0m[92m█[0m[96m█[0m          [94m█[0m[95m█[0m[91m█[0m          [93m█[0m[92m█[0m[96m█[0m    [94m█[0m[95m█[0m[91m█[0m   [93m█[0m[92m█[0m[96m█[0m    [94m█[0m[95m█[0m[91m█[0m 
  [93m█[0m[92m█[0m[96m█[0m    [94m█[0m[95m█[0m[91m█[0m [93m█[0m[92m▀[0m    [96m▄[0m[94m█[0m[95m█[0m[91m█[0m[93m█[0m[92m▀[0m       [96m▄[0m[94m█[0m[95m█[0m[91m█[0m[93m█[0m[92m▀[0m        [96m█[0m[94m█[0m[95m█[0m[91m█[0m[93m█[0m[92m█[0m[96m█[0m[94m█[0m[95m█[0m[91m█[0m   [93m█[0m[92m█[0m[96m█[0m    [94m█[0m[95m█[0m[91m█[0m 
  [93m█[0m[92m█[0m[96m█[0m    [94m█[0m[95m█[0m[91m█[0m                                               [93m█[0m[92m█[0m[96m█[0m    [94m█[0m[95m█[0m[91m█[0m 
                

'''
print(main_logo)

# Ensure download directories exist
os.makedirs('./downloads-audio', exist_ok=True)
os.makedirs('./downloads-video', exist_ok=True)
os.makedirs('./downloads-stream', exist_ok=True)

# Function to print with colors
def cprint(text, color='blue', attrs=['bold']):
    print(colored(text, color, attrs=attrs))

# Convert bytes to human-readable size
def format_size(size):
    if size == 0:
        return "0B"
    power = 1024
    n = 0
    labels = ['B', 'KB', 'MB', 'GB', 'TB']
    while size > power and n < len(labels) - 1:
        size /= power
        n += 1
    return f"{size:.2f} {labels[n]}"

# Convert seconds to ETA (human-readable format)
def format_eta(seconds):
    if seconds < 60:
        return f"{seconds:.0f} sec"
    elif seconds < 3600:
        return f"{seconds // 60:.0f} min {seconds % 60:.0f} sec"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours:.0f} hr {minutes:.0f} min"

# Progress bar hook function
def progress_hook(d):
    if d['status'] == 'downloading':
        size_bytes = d.get('downloaded_bytes', 0) or 0
        total_size_bytes = d.get('total_bytes', 0) or 0
        total_size_mb = format_size(total_size_bytes)
        downloaded_mb = format_size(size_bytes)
        
        # Ensure download speed is not None
        download_speed = format_size(d.get('speed') or 0)
        eta = format_eta(d.get('eta', 0) or 0)
        progress = d.get('progress', 0) * 100 if 'progress' in d else (size_bytes / total_size_bytes * 100 if total_size_bytes else 0)

        # Print in your desired format
        sys.stdout.write(f"\r{colored('Downloading:', 'cyan', attrs=['bold'])} {progress:.2f}% at {download_speed}/s (ETA: {eta}, Size: {total_size_mb})")
        sys.stdout.flush()
        
    elif d['status'] == 'finished':
        sys.stdout.write(f"\r{colored('Download completed!', 'green', attrs=['bold'])}\n")
        sys.stdout.flush()


# Gracefully exit and finalize download on Ctrl+C
def signal_handler(sig, frame):
    cprint("\nCtrl+C detected. Finalizing the download...", 'yellow')
    raise KeyboardInterrupt  # Allows yt-dlp to handle graceful shutdown

# Attach signal handler for Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

# Function to download streams
def download_stream(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': './downloads-stream/%(title)s.%(ext)s',
        'progress_hooks': [progress_hook],
        'concurrent-fragments': 1,  # Sequential download of video/audio fragments
        'continuedl': True  # Enable resuming the download if interrupted
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except KeyboardInterrupt:
        cprint("\nDownload interrupted. The file has been saved.", 'yellow')

# Function to download media (video/audio)
def download_media(url, download_type='video', is_playlist=False):
    ydl_opts = {
        'progress_hooks': [progress_hook],
        'concurrent-fragments': 1,  # Sequential download of video/audio fragments
        'continuedl': True  # Enable resuming the download if interrupted
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

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except KeyboardInterrupt:
        cprint("\nDownload interrupted. The file has been saved.", 'yellow')

# Main menu function
def main():
    while True:
        # Display the menu
        cprint("https://github.com/noarche/youtube-ripper", color='blue')
        cprint("Make a selection for audio or video & playlist. Leave options blank for quick default setting.", color='magenta')
        cprint("Enter the link and wait until prompted for another link!!", color='red')
        cprint("When downloading a stream press CTRL+C to stop recording and save the video.", color='magenta')
        cprint("The same settings will be used for the next link unless you return to the menu.", color='red')
        cprint("Return to the menu to start over by typing 'm' or 'menu' instead of another link.", color='yellow')
        cprint("\n", color='blue')
        cprint("1: Download Video", color='green')
        cprint("2: Download Audio", color='green')
        cprint("3: Download Stream", color='green')

        choice = input(colored("Enter your choice (1-3): ", 'cyan', attrs=['bold'])).strip() or '1'
        is_playlist_input = input(colored("Is this a playlist? (y/n): ", 'cyan', attrs=['bold'])).strip().lower() if choice != '3' else None
        is_playlist = is_playlist_input == 'y' if is_playlist_input else False
        download_type = 'video' if choice == '1' else 'audio' if choice == '2' else 'stream'

        while True:
            url = input(colored("Enter the URL (type 'menu'/'m' to return to the menu, 'exit'/'e' to exit): ", 'cyan', attrs=['bold'])).strip()

            if url.lower() in ['exit', 'e']:
                cprint("Exiting...", color='red')
                return
            elif url.lower() in ['menu', 'm']:
                break  # Go back to the main menu
            else:
                if download_type == 'stream':
                    download_stream(url)
                else:
                    download_media(url, download_type=download_type, is_playlist=is_playlist)
                cprint(f"{download_type.capitalize()} download completed!", color='green')

if __name__ == "__main__":
    main()

