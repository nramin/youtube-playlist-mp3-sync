from bs4 import BeautifulSoup
import os
import requests
import re
#import subprocess

class YoutubePlaylistMp3Sync:

    def __init__(self):
        self.youtube_playlist_url = "http://www.youtube.com/playlist?list="
        self.youtube_root = "http://www.youtube.com"
        self.playlist_cache_folder = os.path.dirname(os.path.realpath(__file__)) + "/cache"
        self.__directory_check(self.playlist_cache_folder)
        self.music_folder = ""
        os.chdir(os.path.dirname(os.path.realpath(__file__)))

    def __directory_check(self, directory):
        if not os.path.exists(os.path.normpath(directory)):
            os.makedirs(os.path.normpath(directory))

    def set_music_folder(self, music_folder="music"):
        if music_folder is "music":
            self.music_folder = os.path.normpath(os.path.dirname(os.path.realpath(__file__)) + "/music")
        else:
            self.music_folder = os.path.normpath(music_folder)
        self.__directory_check(self.music_folder)

    def removeNonAscii(self, s): return "".join(i for i in s if ord(i)<128)

    def filename_parser(self, filename):
        filename = re.sub("[:/?*|<>]", "", filename)
        filename = filename.replace('"', '')
        filename = filename.replace("'", "")
        filename = self.removeNonAscii(filename)
        return filename

    def sync_playlist(self, playlist_id):
        if self.youtube_playlist_url in playlist_id:
            playlist_id = playlist_id.split(self.youtube_playlist_url)[-1]
            playlist_id = playlist_id.split("&")[0]
        r = requests.get(self.youtube_playlist_url + playlist_id)
        playlist_data = BeautifulSoup(r.text)
        playlist_name = self.filename_parser(playlist_data.find("h2", "epic-nav-item-heading").text)
        playlist_location = os.path.normpath(self.music_folder + "/" + playlist_name)
        print("Syncing the Youtube playlist '" + playlist_name + "' with " + playlist_location + "\n")
        playlist_cache = []
        try:
            with open(os.path.normpath(self.playlist_cache_folder + "/" + playlist_id)):
                playlist_cache = [line.strip() for line in
                                  open(os.path.normpath(self.playlist_cache_folder + "/" + playlist_id), 'r')]
                playlist_cache_file = open(os.path.normpath(self.playlist_cache_folder + "/" + playlist_id), 'a+b')
        except IOError:
            playlist_cache_file = open(os.path.normpath(self.playlist_cache_folder + "/" + playlist_id), 'w+')
            self.__directory_check(self.music_folder + "/" + playlist_name)

        synced_tracks_count = 0
        for playlist_video in playlist_data.find_all("a", "ux-thumb-wrap"):
            playlist_video_title = self.filename_parser(playlist_video["title"])
            playlist_video_address = playlist_video["href"].split("&")[0]
            playlist_video_id = playlist_video_address.split("=")[-1]
            if playlist_video_title != "[Deleted Video]" and playlist_video_title != "[Private Video]" \
                and playlist_video_id not in playlist_cache:
                synced_tracks_count += 1
                playlist_cache_file.write(playlist_video_id + "\n")
                print(str(synced_tracks_count) + ". Downloading the video for '" + playlist_video_title + "'...")
                #subprocess.call(os.path.normpath(os.path.dirname(os.path.realpath(__file__)) + "/libraries/youtube-dl.exe") + " --no-part -o temp.%(ext)s " + self.youtube_root + playlist_video_address, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
                os.system(os.path.normpath(os.path.dirname(os.path.realpath(__file__)) + "/libraries/youtube-dl.exe") + " --no-part -o temp.%(ext)s " + self.youtube_root + playlist_video_address)
                if os.path.isfile("temp.mp4"):
                    temp_file = "temp.mp4"
                else:
                    temp_file = "temp.flv"
                print("   Converting the video for '" + playlist_video_title + "' into MP3 format...\n")
                #subprocess.call(os.path.normpath(os.path.dirname(os.path.realpath(__file__)) + "/libraries/ffmpeg.exe") + ' -i temp.mp4 -q:a 0 -map a "' + os.path.normpath(self.music_folder + "/" + playlist_name + "/" + playlist_video_title + '.mp3"'), stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
                os.system(os.path.normpath(os.path.dirname(os.path.realpath(__file__)) + "/libraries/ffmpeg.exe") + ' -i ' + temp_file + ' -q:a 0 -map a "' + os.path.normpath(self.music_folder + "/" + playlist_name + "/" + playlist_video_title + '.mp3"'))
                os.remove(temp_file)
        if synced_tracks_count == 0:
            print("No new songs were added to the Youtube playlist '" + playlist_name + "' from the last time you synced with it.")
        print(str(synced_tracks_count) + " new song(s) were synced from this Youtube playlist to your local MP3 copy of the playlist.")

def main():
    playlist = YoutubePlaylistMp3Sync()
    playlist.set_music_folder("C:/Users/Ramin/Dropbox/youtube-music")
    #playlist.set_music_folder()
    playlist.sync_playlist("PLDgBAt05sRzB3PClMUDYWq9yt5RT0hV5Z")
    playlist.sync_playlist("PLDgBAt05sRzDHen2nVn5UrnnbGSMgmzVq")
    playlist.sync_playlist("PLDgBAt05sRzDH6rMvRhJUVbhSz0KAq5gL")
    playlist.sync_playlist("PLDgBAt05sRzCMrNoLQkEjSlvZH2ob05bX")
    playlist.sync_playlist("PLDgBAt05sRzB-IQYNw5_Wy9wnbnMPfrW1")

if __name__ == "__main__":
    main()