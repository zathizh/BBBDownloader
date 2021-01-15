#! /usr/bin/python3

import requests
import re
import argparse
import os.path
import sys
import time

# VERSION : 1.0.0.1
# AUTHOR  : Sathish Bowatta

# --- GLOBALS ---
_CHUNK_SIZE=1024

# --- PATH SEPERATOR ---
def get_separator():
    platform = sys.platform.lower()

    if platform == "linux" or "darwin":
        sep = "/"
    elif platform == "windows":
        sep = "\\"
    else :
        exit("[-] Invalid Platform")
    return str(sep)

# --- DOWNLOAD WEBM ---
def video_downloader(_url, _id, _dest):
    global CHUNK_SIZE
    file_name = _dest + get_separator() + _id  + ".webm"

    with requests.get(_url, stream=True) as response:
        with open(file_name, 'wb') as f:
            for chunk in response.iter_content(chunk_size=_CHUNK_SIZE):
                f.write(response.content)
# --- MAIN ---
def main():
    parser = argparse.ArgumentParser(prog="BBBVideoDownloader")
    parser.add_argument("-u", "--url", dest="url", action="store", type=str, required=True, help="Meeting URL")
    parser.add_argument("-d", "--dest", dest="dest", action="store", type=str, required=True, help="Download Directory")

    args = parser.parse_args()
    url  = args.url
    dest = args.dest

    meeting_url = str(re.sub("playback\/[a-zA-Z0-9\.\/]*\?meetingId=", "presentation/", url)) + "/deskshare/deskshare.webm"
    meeting_id = url.split("=")[1]

    video_downloader(meeting_url, meeting_id, dest)

if __name__ == '__main__':
    main()

