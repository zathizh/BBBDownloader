#! /usr/bin/python3

import requests
import re
import argparse
import os
import sys

# VERSION : 1.0.0.1
# AUTHOR  : Sathish Bowatta

# --- OS PLATFORM ---
def get_platform():
    return sys.platform.lower()

# --- PATH SEPERATOR ---
def get_separator():
    platform = get_platform()
    sep = ""
    if platform == "linux" or "darwin" :
        sep = "/"
    elif platform == "win32" or platform == "windows" :
        sep = "\\"
    else :
        exit("[-] Invalid Platform")
    return str(sep)

# --- DOWNLOAD WEBM FILES ---
def downloader(_url, path, name, _id):
    file_name =  path + get_separator() + name

    print("[+] Downloading : ", end="")
    print(_url)

    with requests.get(_url) as response:
        with open(file_name, 'wb') as f:
            f.write(response.content)

# --- CREATE OUTPUT DIRECTORY ---
def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

# --- MP4 PROCESSOR ---
def mp4_processor(path, _id):
    platform = get_platform()

    if platform == "linux":
        gen_audio_cmd = "ffmpeg -i " + fpath + "webcams.webm -vn -acodec copy " + fpath + "audio_out.opus"
        prep_mp4_cmd = "ffmpeg -i " + fpath + "deskshare.webm -i " + fpath + "audio_out.opus -map 0:v -map 1:a -c copy -y " + fpath + _id + ".webm"
        os.system(gen_audio_cmd)
        os.system(prep_mp4_cmd)

    elif platform == "win32" or platform == "windows" :
        gen_audio_cmd = ".\\bin\\ffmpeg.exe -i " + fpath + "webcams.webm -vn -acodec copy " + fpath + "audio_out.opus"
        prep_mp4_cmd = ".\\bin\\ffmpeg.exe -i " + fpath + "deskshare.webm -i " + fpath + "audio_out.opus -map 0:v -map 1:a -c copy -y " + fpath + _id + ".webm"
        os.system(gen_audio_cmd)
        os.system(prep_mp4_cmd)

    else :
        print("[-] Invalid Platform, Unable to convert files !!!")
        exit()

def cleanup(path):
    platform = get_platform()
    fpath
    if platform == "linux" or platform == "darwin":
        rm_audio_cmd = "rm -rf " + path + "audio_out.opus"
        rm_deskshare_cmd = "rm -rf " + path + "deskshare.webm"
        rm_deskshare_cmd = "rm -rf " + path + "webcams.webm"
        os.system(rm_audio_cmd)
        os.system(rm_deskshare_cmd)
        os.system(rm_deskshare_cmd)
    elif platform == "win32" or platform == "windows" :
        rm_audio_cmd = "del /f " + path + "audio_out.opus"
        rm_deskshare_cmd = "del /f " + path + "deskshare.webm"
        rm_deskshare_cmd = "del /f " + path + "webcams.webm"
        os.system(rm_audio_cmd)
        os.system(rm_deskshare_cmd)
        os.system(rm_deskshare_cmd)
    else : 
        print("[-] Invalud Platform, Unable to delete files")
        exit()


# --- MAIN FUNCTION ---
def main():
    parser = argparse.ArgumentParser(prog="BBBVideoDownloader")
    parser.add_argument("-u", "--url", dest="url", action="store", type=str, required=True, help="Meeting URL")

    args = parser.parse_args()
    url  = args.url

    meeting_deskshare_url = str(re.sub("playback\/[a-zA-Z0-9\.\/]*\?meetingId=", "presentation/", url)) + "/deskshare/deskshare.webm"
    meeting_webcam_url = str(re.sub("playback\/[a-zA-Z0-9\.\/]*\?meetingId=", "presentation/", url)) + "/video/webcams.webm"
    meeting_id = url.split("=")[1]

    path = "output" + get_separator() + meeting_id + get_separator()
    create_directory(path)

    downloader(meeting_deskshare_url, path, "deskshare.webm", meeting_id)
    downloader(meeting_webcam_url, path, "webcams.webm", meeting_id)

    mp4_processor(path, meeting_id)

    cleanup(path)

if __name__ == '__main__':
    main()
