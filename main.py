# Imports
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Input date
# TODO: make it error resistant
date = input("Which year do you want to travel to? Type the date in the format YYYY-MM-DD")

# Request website contents with exception catching.
# TODO: exception catching seems not to work, as probably entering a date in a wrong format doesn't return an error
#       when requesting. Fix it by making the input error resistant as above and delete the exception catching block
#       here.
try:
    r = requests.get(f"https://www.billboard.com/charts/hot-100/{date}/")
except:
    print ("You have entered a wrong date")
    quit()

# Get text
website = r.text

# Parse the website
soup = BeautifulSoup(website, "html.parser")

# Prettify the soup
prettified_soup = soup.prettify()

# Get titles
titles = soup.findAll(name="h3", class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only", id="title-of-a-story")

# Get title list
title_list = []
for title in titles:
    title_truncated = title.text.replace("\n", "")
    title_list.append(title_truncated)

# Get number 1
number_one = soup.find(name="h3", class_="c-title a-font-primary-bold-l a-font-primary-bold-m@mobile-max lrv-u-color-black u-color-white@mobile-max lrv-u-margin-r-150", id="").text
number_one = number_one.replace("\n", "")

# Insert number 1 in the title list
title_list.insert(0, number_one)

# Get artists
artists = soup.findAll(name="span", class_="c-label a-no-trucate a-font-primary-s lrv-u-font-size-14@mobile-max u-line-height-normal@mobile-max u-letter-spacing-0021 lrv-u-display-block a-truncate-ellipsis-2line u-max-width-330 u-max-width-230@tablet-only")

# Get title list
artist_list = []
for artist in artists:
    artist_truncated = artist.text.replace("\n", "")
    artist_list.append(artist_truncated)

# Get artist no. 1
number_one_artist = soup.find(name="p", class_="c-tagline a-font-primary-l a-font-primary-m@mobile-max lrv-u-color-black u-color-white@mobile-max lrv-u-margin-tb-00 lrv-u-padding-t-025 lrv-u-margin-r-150").text

# Insert number 1 in the artist list
artist_list.insert(0, number_one_artist)

# Create the DataFrame
top_hundred = pd.DataFrame({"Song": title_list, "Artist": artist_list})


