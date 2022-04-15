# Imports
import pandas as pd
import requests
import spotipy
from bs4 import BeautifulSoup
import re
import datetime as dt

# Client ID and secret
SPOTIPY_CLIENT_ID = '6b8a677697c344a18c84a7f5620653e3'
SPOTIPY_CLIENT_SECRET = '5bf92f728c4a4cf2ae67910796257d4a'
SPOTIPY_REDIRECT_URI = 'http://example.com'

# Input date
correct_date = False
while not correct_date:
    date = input("Which year do you want to travel to? Type the date in the format YYYY-MM-DD: ")
    matched = re.match("[1-2][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]", date)
    correct_date: bool = bool(matched)
    if not correct_date:
        print("Error!")
        continue
    year = int(date[0:4])
    month = int(date[5:7])
    day = int(date[8:])
    if year < 1958 or \
            year > dt.date.today().year or \
            year == 1958 and month < 4 or \
            (year == 1958 and month == 8 and day < 4) or \
            month > 12 or \
            month in [1, 3, 5, 7, 8, 10, 12] and day > 31 or \
            month not in [1, 3, 5, 7, 8, 10, 12] and day > 30:
        print("Error!")
        correct_date = False
    else:
        correct_date = True

# Request website contents with exception catching.
r = requests.get(f"https://www.billboard.com/charts/hot-100/{date}/")

# Get text
website = r.text

# Parse the website
soup = BeautifulSoup(website, "html.parser")

# Prettify the soup
prettified_soup = soup.prettify()

# Get titles
titles = soup.findAll(name="h3",
                      class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only",
                      id="title-of-a-story")

# Get title list
title_list = []
for title in titles:
    title_truncated = title.text.replace("\n", "")
    title_truncated = title_truncated.replace("\t", "")
    title_list.append(title_truncated)

# Get number 1
number_one = soup.find(name="h3",
                       class_="c-title a-font-primary-bold-l a-font-primary-bold-m@mobile-max lrv-u-color-black u-color-white@mobile-max lrv-u-margin-r-150",
                       id="").text
number_one = number_one.replace("\n", "")
number_one = number_one.replace("\t", "")

# Insert number 1 in the title list
title_list.insert(0, number_one)

# Get artists
artists = soup.findAll(name="span",
                       class_="c-label a-no-trucate a-font-primary-s lrv-u-font-size-14@mobile-max "
                              "u-line-height-normal@mobile-max u-letter-spacing-0021 lrv-u-display-block "
                              "a-truncate-ellipsis-2line u-max-width-330 u-max-width-230@tablet-only")

# Get title list
artist_list = []
for artist in artists:
    artist_truncated = artist.text.replace("\n", "")
    artist_truncated = artist_truncated.replace("\t", "")
    artist_list.append(artist_truncated)

# Get artist no. 1
number_one_artist = soup.find(name="p",
                              class_="c-tagline a-font-primary-l a-font-primary-m@mobile-max lrv-u-color-black u-color-white@mobile-max lrv-u-margin-tb-00 lrv-u-padding-t-025 lrv-u-margin-r-150").text

# Insert number 1 in the artist list
artist_list.insert(0, number_one_artist)

# Create a DataFrame of top hundred songs
top_hundred = pd.DataFrame({"Song": title_list, "Artist": artist_list})
top_hundred.index += 1
print(top_hundred)

# Save the DataFrame to Excel
top_hundred.to_excel(f"Top Hundred {date}.xlsx")


# Create SpotifyOAuth object
oauth = spotipy.oauth2.SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                    client_secret=SPOTIPY_CLIENT_SECRET,
                                    redirect_uri=SPOTIPY_REDIRECT_URI,
                                    show_dialog=True,
                                    scope="playlist-modify-public",
                                    cache_path="token.txt")

# Get current user ID
# Create a Spotify object
sp = spotipy.Spotify(oauth_manager=oauth)

# Get my ID
my_id = sp.me()['id']

# Create an URI list
uri_list = []

for index in range(100, 1, -1):
    try:
        uri_list.append(sp.search(q=f"artist:{top_hundred.Artist[index]} track:{top_hundred.Song[index]}",
                                  type="track")['tracks']['items'][0]['uri'])
    except IndexError:
        continue

print(uri_list)

# # Create playlist
playlist = sp.user_playlist_create(user=my_id, name=f"Billboard Top 100 {date}")
sp.playlist_add_items(playlist_id=playlist['id'], items=uri_list)
print(f"Playlist for Billboard Top 100 from {date} created!")