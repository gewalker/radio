#!/usr/bin/env python3
"""
    A random song player for google play music.
"""


from gmusicapi import Mobileclient
import random
import subprocess
import time
import pickle
import os
from sys import argv 

api = Mobileclient()

def musiclogin(api):
    try:
        logged_in = api.login(argv[1], argv[2], '0101010101010101')
    except gmusicapi.exceptions.AlreadyLoggedIn:
        pass

def getsongs(api):
    if os.path.isfile('mysongfile.pkl'):
        print("Loading song db from file.")
        pkl_file = open('mysongfile.pkl', 'rb')
        songs = pickle.load(pkl_file)
        return songs
    else:
        print("Acquiring song db from Google.")
        try:
            songs = api.get_all_songs()
            output = open('mysongfile.pkl', 'wb')
            pickle.dump(songs, output)
            output.close()
            return songs
        except gmusicapi.exceptions.NotLoggedIn:
            print("Whoops, not logged in.\n")
            self.musiclogin()
            getsongs(api)

musiclogin(api)
songs = getsongs(api)
while True:
    try:
        song = random.choice(songs)
        if song['genre'] in ["Audio Book", "Classical", "Doom Metal", "Opera", "Podcast", "Educational"]:
            print("You probably don't want to hear {s}. Picking another one.".format(s=song['title']))
            continue
        songurl = 'http' + api.get_stream_url(song['id']).lstrip('https')
        print("Playing " + song['title'] + " by " + song['artist'] + " from album " + song['album'] +".\n")
        player = subprocess.Popen(['mpg321', songurl])
        while player.poll() is None:
            time.sleep(1)
            continue
    except KeyboardInterrupt:
        input("Press Enter to play next song, ^C to exit.")
        continue
