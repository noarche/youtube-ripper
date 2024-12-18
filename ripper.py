import yt_dlp
import os
from termcolor import colored
import sys
import signal
import argparse

PROXY_IP = '127.0.0.1'
PROXY_PORT = 9150
AUDIO_DOWNLOAD_DIR = './downloads-audio'
VIDEO_DOWNLOAD_DIR = './downloads-video'
STREAM_DOWNLOAD_DIR = './downloads-stream'

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

os.makedirs(AUDIO_DOWNLOAD_DIR, exist_ok=True)
os.makedirs(VIDEO_DOWNLOAD_DIR, exist_ok=True)
os.makedirs(STREAM_DOWNLOAD_DIR, exist_ok=True)

def cprint(text, color='blue', attrs=['bold']):
    print(colored(text, color, attrs=attrs))

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

def format_eta(seconds):
    if seconds < 60:
        return f"{seconds:.0f} sec"
    elif seconds < 3600:
        return f"{seconds // 60:.0f} min {seconds % 60:.0f} sec"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours:.0f} hr {minutes:.0f} min"

def progress_hook(d):
    if d['status'] == 'downloading':
        size_bytes = d.get('downloaded_bytes', 0) or 0
        total_size_bytes = d.get('total_bytes', 0) or 0
        total_size_mb = format_size(total_size_bytes)
        downloaded_mb = format_size(size_bytes)

        download_speed = format_size(d.get('speed') or 0)
        eta = format_eta(d.get('eta', 0) or 0)
        progress = d.get('progress', 0) * 100 if 'progress' in d else (size_bytes / total_size_bytes * 100 if total_size_bytes else 0)

        sys.stdout.write(f"\r{colored('Downloading:', 'cyan', attrs=['bold'])} {progress:.2f}% at {download_speed}/s (ETA: {eta}, Size: {total_size_mb})")
        sys.stdout.flush()

    elif d['status'] == 'finished':
        sys.stdout.write(f"\r{colored('Download completed!', 'green', attrs=['bold'])}\n")
        sys.stdout.flush()

def signal_handler(sig, frame):
    cprint("\nCtrl+C detected. Finalizing the download...", 'yellow')
    raise KeyboardInterrupt

signal.signal(signal.SIGINT, signal_handler)

def download_stream(url, proxy=None):
    ydl_opts = {
        'format': 'best',
        'outtmpl': f'{STREAM_DOWNLOAD_DIR}/%(title)s.%(ext)s',
        'progress_hooks': [progress_hook],
        'concurrent-fragments': 1,
        'continuedl': True
    }

    if proxy:
        ydl_opts['proxy'] = proxy

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except KeyboardInterrupt:
        cprint("\nDownload interrupted. The file has been saved.", 'yellow')

def download_media(url, download_type='video', is_playlist=False, proxy=None):
    ydl_opts = {
        'progress_hooks': [progress_hook],
        'concurrent-fragments': 1,
        'continuedl': True
    }

    if download_type == 'video':
        ydl_opts.update({
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': f'{VIDEO_DOWNLOAD_DIR}/%(title)s.%(ext)s',
        })
    elif download_type == 'audio':
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': f'{AUDIO_DOWNLOAD_DIR}/%(title)s.%(ext)s',
        })

    ydl_opts['noplaylist'] = not is_playlist

    if proxy:
        ydl_opts['proxy'] = proxy

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        cprint(f"Error downloading {url}: {e}", 'red')

def process_file(file_path, download_type='video', proxy=None):
    try:
        with open(file_path, 'r') as file:
            links = file.readlines()
            for url in links:
                url = url.strip()
                if not url:
                    continue
                cprint(f"Processing URL: {url}", 'cyan')
                download_media(url, download_type=download_type, is_playlist=False, proxy=proxy)
    except Exception as e:
        cprint(f"Error reading file: {e}", 'red')

def main():
    parser = argparse.ArgumentParser(description="Media Ripper with optional Tor proxy support.")
    parser.add_argument('-tor', action='store_true', help="Route all traffic through Tor proxy")
    parser.add_argument('-file', type=str, help="Path to a text file containing URLs to download")
    args = parser.parse_args()

    proxy = None
    if args.tor:
        proxy = f"socks5://{PROXY_IP}:{PROXY_PORT}"
        cprint(f"Using Tor proxy: {proxy}", color='yellow')

    if args.file:
        cprint(f"Downloading from file: {args.file}", color='blue')
        process_file(args.file, download_type='video', proxy=proxy)
        return

    while True:
        cprint("Media Ripper | Audio | Video | Stream | Highest Quality | Any Website ", color='blue')
        cprint("Make a selection for audio or video & playlist. Leave options blank for quick default setting.", color='magenta')
        cprint("Enter the link and wait until prompted for another link!!", color='red')
        cprint("When downloading a stream press CTRL+C to stop recording and save the video.", color='magenta')
        cprint("The same settings will be used for the next link unless you return to the menu.", color='red')
        cprint("Return to the menu to start over by typing 'm' or 'menu' instead of another link.", color='yellow')
        cprint("To download over TOR use '-tor' argument when running this script. ", color='blue')
        cprint("Start batch video download from list of links with '-file anyTextFile.txt' ", color='blue')
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
                break
            else:
                if download_type == 'stream':
                    download_stream(url, proxy=proxy)
                else:
                    download_media(url, download_type=download_type, is_playlist=is_playlist, proxy=proxy)
                cprint(f"{download_type.capitalize()} download completed!", color='green')

if __name__ == "__main__":
    main()
