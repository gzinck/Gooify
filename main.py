from gmus import *
from spotify import *
import datetime

gmus = GMusicClient()
spot = SpotifyClient()

print()
print('--------------------------------------------------------------------')
print('Gooify: Main Menu')
print('--------------------------------------------------------------------')
print('Type "copy all" to copy your entire library from GMusic to Spotify.')
print('Type "copy playlists" to copy every playlist from GMusic to Spotify.')
print('Follow the command with a number to indicate the index to start from,')
print('     if the first tracks were already processed.')
print('     Example: "copy all 4" skips the first 4 tracks.')
print('Type "exit" to quit.')
print('--------------------------------------------------------------------')
userInput = input()
log = open("error-log.txt","a+")
while(userInput != 'exit'):
    if(userInput[:8] == 'copy all'):
        log.write('\n\nCOPY ALL OPERATION ERRORS\n' + datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y") + '\n--------------\n')
        library = gmus.get_all()

        # Skip a few places, if applicable
        if(len(userInput) > 9):
            library.start_from(int(userInput[9:]))
            print('Skipping the first', userInput[9:], 'tracks.')

        for song in library:
            if(not spot.add_song(song)):
                log.write(song['title'] + ' by ' + song['artist'] + ' in album ' + song['album'] + '\n')

    if(userInput[:14] == 'copy playlists'):
        log.write('\nCOPY PLAYLIST OPERATION ERRORS\n' + datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y") + '\n--------------\n')
        # Get all playlists in the google music library
        playlists = gmus.get_playlists()

        # Skip a few places, if applicable
        if(len(userInput) > 15):
            playlists.start_from(int(userInput[15:]))
            print('Skipping the first', userInput[15:], 'playlists.')

        for playlist in playlists:
            name = playlist.get_name()
            id = spot.add_playlist(name)
            for song in playlist:
                if(not spot.add_song_to_playlist(id, song)):
                    log.write(name + ': ' + song['title'] + ' by ' + song['artist'] + ' in album ' + song['album'] + '\n')

    print()
    print('--------------------------------------------------------------------')
    print('Gooify: Main Menu')
    print('--------------------------------------------------------------------')
    print('Type "copy all" to copy your entire library from GMusic to Spotify.')
    print('Type "copy playlists" to copy every playlist from GMusic to Spotify.')
    print('Type "exit" to quit.')
    print('--------------------------------------------------------------------')
    userInput = input()

log.close()
print('--------------------------------------------------------------------')
print('See you later!')
print('--------------------------------------------------------------------')
