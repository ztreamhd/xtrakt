#!/usr/bin/python3

banner = r'''
#########################################################################
#      YouTube to M3U8 Grabber                                         #
#      Updated to use yt-dlp for reliable stream extraction            #
#########################################################################
'''

import subprocess
import os
import sys

def grab(url):
    """
    Use yt-dlp to extract the actual m3u8 stream URL from a YouTube live stream.
    """
    try:
        result = subprocess.run(
            [
                'yt-dlp',
                '--no-download',          # Don't download the video
                '-f', 'best',             # Best available format
                '--print', 'url',         # Print just the direct URL
                url
            ],
            capture_output=True,
            text=True,
            timeout=30
        )

        stream_url = result.stdout.strip()

        if stream_url and ('http' in stream_url):
            print(stream_url)
        else:
            # Log stderr for debugging
            sys.stderr.write(f"[WARN] No stream found for {url}\n")
            if result.stderr:
                sys.stderr.write(f"  yt-dlp error: {result.stderr.strip()}\n")
            print('https://raw.githubusercontent.com/benmoose39/YouTube_to_m3u/main/assets/moose_na.m3u')

    except subprocess.TimeoutExpired:
        sys.stderr.write(f"[WARN] Timeout grabbing {url}\n")
        print('https://raw.githubusercontent.com/benmoose39/YouTube_to_m3u/main/assets/moose_na.m3u')
    except FileNotFoundError:
        sys.stderr.write("[ERROR] yt-dlp not found! Install it first.\n")
        print('https://raw.githubusercontent.com/benmoose39/YouTube_to_m3u/main/assets/moose_na.m3u')
    except Exception as e:
        sys.stderr.write(f"[ERROR] {e}\n")
        print('https://raw.githubusercontent.com/benmoose39/YouTube_to_m3u/main/assets/moose_na.m3u')


print('#EXTM3U x-tvg-url="https://github.com/botallen/epg/releases/download/latest/epg.xml"')
print(banner)

with open('../youtube_channel_info.txt') as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('~~'):
            continue
        if not line.startswith('https:'):
            line = line.split('|')
            ch_name   = line[0].strip()
            grp_title = line[1].strip().title()
            tvg_logo  = line[2].strip()
            tvg_id    = line[3].strip()
            print(f'\n#EXTINF:-1 group-title="{grp_title}" tvg-logo="{tvg_logo}" tvg-id="{tvg_id}", {ch_name}')
        else:
            grab(line)

# Clean up any temp files
if os.path.exists('temp.txt'):
    os.remove('temp.txt')
