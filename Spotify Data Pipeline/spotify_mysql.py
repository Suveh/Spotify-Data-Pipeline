import re
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import mysql.connector

# Set up Spotify API credentials
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id='71f8ce698b334fb1a1ac028e577c9631',
    client_secret='c8fdf1c537af4481adaf8126c3740b42'
))

#MySQL Database connection
db_config={
    'host':'localhost',
    'user':'root',
    'password':'Suve@2002',
    'database':'spotify_db',
}

#connect to the database
connection=mysql.connector.connect(**db_config)
cursor=connection.cursor()

#Read track URLs from file
file_path="track_urls.txt"
with open(file_path, 'r') as file:
    track_urls=file.readlines()

#List to store all tracks metadata
all_tracks_data=[]

#Process each URL
for track_url in track_urls:
    track_url=track_url.strip() #remove any leading or trailing whitespace
    try:
        # Extract the track ID
        track_id = re.search(r'track/([a-zA-Z0-9]+)', track_url).group(1)

        # Get full track data from Spotify API
        track = sp.track(track_id)

        #Extract metadata
        track_data={
            'Track Name': track['name'],
            'Album':track['album']['name'],
            'Artist':track['artists'][0]['name'],
            'Popularity':track['popularity'],
            'Duration (minutes)':track['duration_ms']/60000
        }

        #Append to the list
        all_tracks_data.append(track_data)

        #Insert data into MySQL
        insert_query="""
        INSERT INTO spotify_tracks (track_name, artist, album, popularity, duration_minutes)
        VALUES(%s, %s, %s, %s, %s)"""

        cursor.execute(insert_query, (
            track_data['Track Name'],
            track_data['Artist'],
            track_data['Album'],
            track_data['Popularity'],
            track_data['Duration (minutes)']
        ))
        connection.commit()

    except Exception as e:
        print(f"Error processing URL: {track_url}, Error: {e}")

#CLose the connection
cursor.close()
connection.close()

print("All tracks have been processed and inserted into the database.")
        