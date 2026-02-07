#!/usr/bin/python3

banner = r'''
#########################################################################
#      YouTube to M3U8 Grabber                                         #
#      Uses yt-dlp with Deno JS runtime + cookie support               #
#########################################################################
'''

import subprocess
import os
import sys
import time

COOKIES_FILE = '/tmp/cookies.txt'
FALLBACK_URL = 'https://raw.githubusercontent.com/benmoose39/YouTube_to_m3u/main/assets/moose_na.m3u'

def grab(url):
    """
    Use yt-dlp to extract the m3u8/stream URL from a YouTube live stream.
    """
    try:
        cmd = [
            'yt-dlp',
            '--no-download',
            '--print', 'url',
            '-f', 'b',                    # "b" instead of "best" to suppress warning
            '--no-warnings',              # Suppress non-critical warnings
        ]

        # Add cookies if available
        if os.path.exists(COOKIES_FILE):
            cmd.extend(['--cookies', COOKIES_FILE])

        # Add the URL
        cmd.append(url)

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60  # Increased timeout since JS runtime takes longer
        )

        stream_url = result.stdout.strip()

        # Sometimes yt-dlp returns multiple lines; take the first valid URL
        if stream_url:
            for line in stream_url.splitlines():
                line = line.strip()
                if line.startswith('http'):
                    print(line)
                    return

        # If we get here, no valid URL was found
        sys.stderr.write(f"[WARN] No stream found for {url}\n")
        if result.stderr:
            sys.stderr.write(f"  stderr: {result.stderr.strip()}\n")
        if result.returncode != 0:
            sys.stderr.write(f"  exit code: {result.returncode}\n")
        print(FALLBACK_URL)

    except subprocess.TimeoutExpired:
        sys.stderr.write(f"[WARN] Timeout grabbing {url}\n")
        print(FALLBACK_URL)
    except Exception as e:
        sys.stderr.write(f"[ERROR] {e}\n")
        print(FALLBACK_URL)


print('#EXTM3U x-tvg-url="https://github.com/botallen/epg/releases/download/latest/epg.xml"')
print(banner)

with open('../youtube_channel_info.txt') as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('~~'):
            continue
        if not line.startswith('https:'):
            parts = line.split('|')
            ch_name   = parts[0].strip()
            grp_title = parts[1].strip().title()
            tvg_logo  = parts[2].strip()
            tvg_id    = parts[3].strip()
            print(f'\n#EXTINF:-1 group-title="{grp_title}" tvg-logo="{tvg_logo}" tvg-id="{tvg_id}", {ch_name}')
        else:
            grab(line)
            time.sleep(3)  # Delay to avoid rate limiting / bot detection

# Cleanup
if os.path.exists('temp.txt'):
    os.remove('temp.txt')
