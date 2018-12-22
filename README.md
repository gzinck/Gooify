# Gooify

Gooify is a simple program that finds all of the music in your Google Play Music library and adds it to your Spotify library. It has two options: to copy your entire library to Spotify or to copy all playlists to Spotify.

## Requirements

- Must have python 3 installed along with pip
- Must have installed gmusicapi (a python package for interfacing with Google Play Music)

<code>pip install gmusicapi</code>

- Must have installed spotipy (a python package for interfacing with Spotify)

<code>pip install spotipy</code>

## Usage

1. Install required components
2. <code>cd</code> to the folder with the repository
3. Run <code>main.py</code> using Python 3
4. Enter your credentials for Spotify and Google Play Music. Browser windows will open to verify your credentials if it is your first time using the program.
5. Follow the instructions to either copy your entire library or copy all your playlists. You can opt to copy only songs after a certain index if some were previously copied.

The program is slow and does not support multi-threading due to Spotify's limitations on the developer API which do not allow fast simultaneous queries.

## Limitations

- Some songs cannot be found on Spotify. A number of measures have been taken to minimize this (shortening the song/artist name during search, searching without the album name, etc.). Unfortunately, this does not cover all possibilities and it also slows down the application.
- Karaoke versions are added instead of the actual ones sometimes.
- Playlist transfer does not support songs that were uploaded to Google Play Music, since these songs do not have their track information visible to the API.
- Spotify times out after an hour.
- If songs already existed in a playlist, then the program will add to it (potentially adding duplicates).

## Debugging

- If there were a lot of missed tracks, you can find them in the text file called "error-log.txt", which will be visible after exiting python.
- If the program crashed in the middle of performing its action, you can restart at that track number or playlist. Simply restart the application and append the index to start work. For instance, <code>copy all 699</code> starts at the 700th song, and <code>copy playlists 2</code> starts at the 3rd playlist (index 2, because it is 0-indexed).
