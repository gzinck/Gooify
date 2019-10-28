import sys
import os
import spotipy
import spotipy.util as util

class SpotifyClient:
    def __init__(self):
        """
        This connects to Spotify's servers.
        """
        # This determines what the app has access to do
        scope = 'user-library-read user-library-modify playlist-modify-private playlist-read-private playlist-modify-public'
        
        username = input('Type your Spotify username below.\n--> ')

        # If used an old scope, we might have to delete the cache
        dir_path = os.path.dirname(os.path.realpath(__file__)) + '/.cache-spotify' + username
        cache = 0
        if(not os.path.isfile(dir_path)):
            cache = open(dir_path, 'w')
            cache.write("v1.0")
            if(os.path.isfile(f".cache-{username}")):
                os.remove(f".cache-{username}") # Only needed if already ran the app in different mode
        else:
            cache = open(dir_path, 'r')
            if(cache.read() != "v1.0"):
                cache.close()
                if(os.path.isfile(f".cache-{username}")):
                    os.remove(f".cache-{username}") # Only needed if already ran the app in different mode
                cache = open(dir_path, 'w')
                cache.write("v1.0")
        cache.close()

        token = util.prompt_for_user_token(username=username, scope=scope, client_id='d2847081cfd04a248bf67b8fcf49b0cf', client_secret='b553b59f9c9f44f69f368c5d94017288', redirect_uri='http://graemezinck.ca/')

        if(token):
            self.api = spotipy.Spotify(auth=token)
            print('Connected to Spotify')
        else:
            print('Can\'t get the token for', username)

    def add_playlist(self, playlist_name):
        """
        Adds a playlist to the library, if not already present.
        """
        usr = self.api.current_user()['id']
        id = self.get_playlist(playlist_name)
        if(id == None):
            self.api.user_playlist_create(user=usr, name=playlist_name, public=False)
            return self.get_playlist(playlist_name)
        else:
            return id

    def get_playlist(self, playlist_name):
        """
        Gets a playlist with a given name and returns its id.
        """
        usr = self.api.current_user()['id']
        p_lists = self.api.user_playlists(user=usr)['items']
        for lst in p_lists:
            if(lst['name'] == playlist_name):
                return lst['id']
        return None

    def add_song_to_playlist(self, playlist_id, track):
        """
        Adds a song to a playlist, specified by its Spotify id.
        """
        usr = self.api.current_user()['id']
        uri = self.get_uri(track)
        if(uri == None):
            return False
        else:
            self.api.user_playlist_add_tracks(user=usr, playlist_id=playlist_id, tracks=[uri])
            print('Added to playlist', playlist_id)
            return True

    def add_song(self, track):
        """
        Adds a track to the Spotify account. Returns if it was
        successfully found on Spotify.
        """
        uri = self.get_uri(track)
        if(uri == None):
            return False
        else:
            # Check if the song is already in the library
            if(self.api.current_user_saved_tracks_contains([uri])[0]):
                print('Song already in library')
            else:
                self.api.current_user_saved_tracks_add([uri])
                print('Added to library')
            return True

    def get_uri(self, track):
        """
        Gets the Spotify URI for the tracks
            return: the Spotify URI
        """
        # Get the song info from Google
        trackname = track['title'].replace("'", "")
        artistname = track['artist'].replace("'", "")
        albumname = track['album'].replace("'", "")

        # Find the song on spotify
        song = self.find_song(trackname, artistname, albumname)

        # If no result, say so.
        if(song == None):
            print('Could not find', trackname, 'by', artistname)
            return None
        else:
            print('Found', song['name'])
            return song['uri']

    def find_song(self, trackname, artistname, albumname):
        """
        Finds a song from Spotify based on the track name and
        artist name. It will shorten the names in order to find
        the closest match, since many will not fit exactly.
            return: Spotify song object
        """
        # Fix the artist name
        artistname = artistname.replace('and', ' ')

        # Fix the title
        translation_table = dict.fromkeys(map(ord, ';/"()&'), ' ')
        artistname = artistname.translate(translation_table)
        trackname = trackname.translate(translation_table)
        albumname = albumname.translate(translation_table)

        string = "track:" + trackname + " artist:" + artistname + " album:" + albumname
        results = self.api.search(q=string, type='track', limit=1)
        items = results['tracks']['items']

        # Shorten the track name until we find a result
        if(len(items) == 0):
            items = self.find_by_shorter_track(trackname, artistname, albumname)

        # Shorten the artist name until we find a result (if no success before)
        if(len(items) == 0):
            items = self.find_by_shorter_artist(trackname, artistname, albumname)

        # Try again without any album name
        if(len(items) == 0):
            items = self.find_by_shorter_track(trackname, artistname)
        if(len(items) == 0):
            items = self.find_by_shorter_artist(trackname, artistname)

        if(len(items) == 0):
            return None
        else:
            return items[0]

    def find_by_shorter_track(self, trackname, artistname, albumname=None):
        """
        Finds a song from Spotify based on the track name and
        artist name, shortening the track name incrementally
        until it finds a track.
            return: list of results, which may be empty
        """
        placeToEnd = len(trackname)
        track = trackname
        items = []

        while(placeToEnd != -1 and len(items) == 0):
            track = track[:placeToEnd]
            string = "track:" + trackname + " artist:" + artistname
            if(albumname != None):
                string += " album:" + albumname
            results = self.api.search(q=string, type='track', limit=1)
            items = results['tracks']['items']
            placeToEnd = track.rfind(' ')
        return items

    def find_by_shorter_artist(self, trackname, artistname, albumname=None):
        """
        Finds a song from Spotify based on the track name and
        artist name, shortening the artist name incrementally
        until it finds a track.
            return: list of results, which may be empty
        """
        placeToEnd = len(trackname)
        artist = artistname
        items = []

        while(placeToEnd != -1 and len(items) == 0):
            artist = artist[:placeToEnd]
            string = "track:" + trackname + " artist:" + artistname
            if(albumname != None):
                string += " album:" + albumname
            results = self.api.search(q=string, type='track', limit=1)
            items = results['tracks']['items']
            placeToEnd = artist.rfind(' ')

        # Case where there is a Various Artists artist
        if(len(items) == 0 and albumname != None):
            string = "track:" + trackname + " album:" + albumname
            results = self.api.search(q=string, type='track', limit=1)
            items = results['tracks']['items']
            
        return items
