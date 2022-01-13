# Imports
import requests
from bs4 import BeautifulSoup

# Input date.
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

# Get title list.
title_list = soup.findAll(name="h3", class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only", id="title-of-a-story")

# TODO:
#  1) Get all titles
#  2) Get number one (different class)
#  3) Get artist names
#  4) Join titles with artist names
#  5) Enumerate
#  6) Get the full list (number, song, artist)



