import os

from spotipy.oauth2 import SpotifyClientCredentials
import sys
import pprint
import re


from flask import Flask, request, redirect, session, url_for, render_template_string
#a session is just a place for our web server in this case flask 
#to be able to access the data inside

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler
#modules we're using to set up our authorisation with Spotipy library and Spotify API


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)
#generating a string of 64 random byte so users can't tamper with data

#variables needed by spotipy
client_id = 'b1ef72a13ae5420da33242a3ac9a23cb'
client_secret = '3eb65dbece034b4bb0931c936e172e0e'
redirect_uri = 'http://localhost:5000/callback'
scope = 'playlist-read-private playlist-modify-private playlist-modify-public user-read-recently-played user-read-playback-state'

cache_handler = FlaskSessionCacheHandler(session)
#store access token in flask session, which is what cache_handler does

sp_oauth = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope,
    cache_handler=cache_handler,
    show_dialog=True
)
#authenticate with spotify web api
#show dialog is for debugging purposes (shows the screen user sees when they are asked to log in)

sp = Spotify(oauth_manager=sp_oauth)
#instance of spotify (spotify client)
#call methods on to get data

@app.route('/')
def home():
    error_message = request.args.get('error_message')  # Get the error message if available
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        #validate token allows us to check if we have a valid token (Stored in flask)
        auth_url = sp_oauth.get_authorize_url()
        #if they havent logged in, get authorise url gets them to the url to get them to log in
        return redirect(auth_url)
    return render_template_string("""
        <h1>Enter Your Playlist Link</h1>
        <form action="/process_playlist" method="post">
            <label for="playlist_url">Spotify Playlist URL:</label><br>
            <input type="text" id="playlist_url" name="playlist_url" required><br><br>
            <input type="submit" value="Submit">
        </form>
        {% if error_message %}
            <div style="color: red; border: 1px solid red; padding: 10px; margin-top: 10px;">
                <strong>Error:</strong> {{ error_message }}
            </div>
        {% endif %}
    """, error_message=error_message)

@app.route('/process_playlist', methods=['POST'])
def process_playlist():
    playlist_url = request.form['playlist_url']
    
    # Extract the playlist ID from the URL
    playlist_id = extract_playlist_id(playlist_url)
    if not playlist_id:
        return redirect(url_for('home', error_message="Invalid Playlist URL. Please try again."))
    
    tracks_info = search_and_add_songs_to_playlist(playlist_id)
    
    # Return the feedback with all songs added, not found, and skipped
    return render_template_string("""
        <h1>Song Processing Feedback</h1>
        <h3>Added to Playlist:</h3>
        <ul>
            {% for track in added_tracks %}
                <li>{{ track | safe }}</li>  <!-- Use 'safe' to render the HTML link correctly -->
            {% endfor %}
        </ul>
        <h3>Could Not Be Found:</h3>
        <ul>
            {% for track in not_found_tracks %}
                <li>{{ track }}</li>
            {% endfor %}
        </ul>
        <h3>Skipped Songs:</h3>
        <ul>
            {% for track in skipped_tracks %}
                <li>{{ track }}</li>
            {% endfor %}
        </ul>
    """, added_tracks=tracks_info['added'], not_found_tracks=tracks_info['not_found'], skipped_tracks=tracks_info['skipped'])

def extract_playlist_id(url):
    # Regular expression to match Spotify playlist URLs
    match = re.search(r"spotify\.com/playlist/([^?&/]+)", url)
    if match:
        return match.group(1)
    else:
        return None

def search_and_add_songs_to_playlist(playlist_id):
    added_tracks = []
    not_found_tracks = []
    skipped_tracks = set()  # To track URIs of already added songs
    added_uris = set()

    # Get existing tracks in the playlist
    playlist_tracks = sp.playlist_tracks(playlist_id)
    for item in playlist_tracks['items']:
        added_uris.add(item['track']['uri'])

    with open('list_of_songs.txt', 'r') as file:
        for line in file:
            query = line.strip().encode('windows-1252').decode('utf-8')
            # Search for the track
            search_results = sp.search(q=query, type='track', limit=1)

            if search_results['tracks']['items']:
                track = search_results['tracks']['items'][0]
                track_name = track['name']
                artist_name = ', '.join([artist['name'] for artist in track['artists']])
                track_url = track['external_urls']['spotify']
                track_uri = track['uri']
                
                # Check if track is already in the playlist
                if track_uri in added_uris:
                    skipped_tracks.add(f"{track_name} by {artist_name}")
                else:
                    # Add track to playlist
                    sp.playlist_add_items(playlist_id=playlist_id, items=[track_uri])
                    added_tracks.append(f"<a href='{track_url}'>{track_name} by {artist_name}</a>")
                    added_uris.add(track_uri)
            else:
                # Track not found
                not_found_tracks.append(query)

    return {'added': added_tracks, 'not_found': not_found_tracks, 'skipped': skipped_tracks}



#refresh token
@app.route('/callback')
def callback():
    sp_oauth.get_access_token(request.args['code'])
    return redirect(url_for('home'))




@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
    #restarts server after making changes so no need to do it manually


#sp.playlist_add_items(playlist_id=playlist_id_new, items=['spotify:episode:3nwfTNjbhDu8Cnp81TdmGO'], position=None)




