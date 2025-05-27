import re
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import json
import pandas as pd
import matplotlib.pyplot as plt

# Set up Spotify API credentials
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id='71f8ce698b334fb1a1ac028e577c9631',
    client_secret='c8fdf1c537af4481adaf8126c3740b42'
))

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

    except Exception as e:
        print(f"Error processing URL: {track_url}, Error: {e}")

#Convert metadata to DAtaFrame
df=pd.DataFrame(all_tracks_data)

#Save metadata to CSV
df.to_csv('spotify_track_data.csv',index=False)

#Save metadata to JSON
with open("spotify_tracks.json","w") as f:
    json.dump(all_tracks_data,f,indent=4)

print("All track data saved to 'spotify_tracks.json' and 'spotify_track_data.csv'")

#Visualize popularity of all tracks
track_name=[track['Track Name'] for track in all_tracks_data]
popularities=[track['Popularity'] for track in all_tracks_data]

plt.figure(figsize=(10,8))
plt.bar(track_name,popularities,color='lightgreen',edgecolor='black')
plt.xticks(rotation=45,ha='right')
plt.title(f"Popularity of all Tracks")
plt.ylabel('Popularity')
plt.show()