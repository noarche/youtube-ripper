import yt_dlp
import os
from termcolor import colored
import sys
import signal

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

# Convert time to human-readable format
def format_time(seconds):
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
        frames = d.get('fragment_index', 0)
        total_frames = d.get('fragment_count', 'Unknown')
        size_bytes = d.get('downloaded_bytes', 0)
        size = format_size(size_bytes)
        time_elapsed = d.get('elapsed', 0)
        sys.stdout.write(f"\r{colored('Frames:', 'cyan')} {frames}/{total_frames} | {colored('Size:', 'green')} {size} | {colored('Time:', 'yellow')} {format_time(time_elapsed)}")
        sys.stdout.flush()
    elif d['status'] == 'finished':
        sys.stdout.write(f"\r{colored('Download completed!', 'green', attrs=['bold'])}\n")
        sys.stdout.flush()

# Gracefully exit and finalize download on Ctrl+C
def signal_handler(sig, frame):
    cprint("\nCtrl+C detected. Finalizing the download...", 'yellow')
    # Signal yt-dlp to complete and finalize the current download
    raise KeyboardInterrupt  # This allows yt-dlp to handle graceful shutdown

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
