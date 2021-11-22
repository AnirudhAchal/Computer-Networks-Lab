# Import requests to fetch the raw HTML data, and BeautifulSoup4 to parse the HTML
import requests
from bs4 import BeautifulSoup

# IMDB URL from where data is to be fetched
IMDB_URL = "https://www.imdb.com/search/title/?groups=top_100&sort=user_rating,desc&count=50"

# HTML Parser to use with BeautifulSoup
HTML_PARSER = "html.parser"

# Formatting related variables
BOLD_START = '\033[1m'
ITALIC_START = '\033[3m'
STYLE_END = '\033[0m'

# Fetch the data from the IMDB URL
req = requests.get(IMDB_URL)

# Initialize the html parser
soup = BeautifulSoup(req.content, HTML_PARSER)

# Iterate through the movies in the fetched list
for child in soup.find_all(class_="lister-item-content"):
    # Print the Movie Rank, Title and Year of Release
    print(BOLD_START + ITALIC_START, end="")
    for ele in child.h3.children:
        innertext = ele.get_text(strip=True)
        if innertext:
            print(innertext, end=" ")
    print(STYLE_END)

    # Print the IMDB Rating for the movie
    rating = child.findChild("div", class_="ratings-bar")
    print(f"{BOLD_START}IMDB Rating:{STYLE_END} " + rating.div.strong.get_text(strip=True))

    # Print the stars acting in the movie
    stars = rating.nextSibling.nextSibling.nextSibling.nextSibling.findChild(class_="ghost")
    for star in stars.next_siblings:
        innertext = star.get_text(strip=True)
        if innertext == "Stars:":
            print(BOLD_START + innertext + STYLE_END, end=" ")
        elif innertext == ",":
            print('\b' + innertext, end=" ")
        elif innertext:
            print(innertext, end=" ")
    print("\n")
