from requests import get
from bs4 import BeautifulSoup
import re
import pandas as pd
from time import sleep
from tqdm import tqdm
import numpy as np


"""
This file includes the code which crawls and
downloads movie pages from FilmKio website.
"""

download_queue = []

# This function find the selects the movie url from the given page
# It has been customized for FilmKio webpages
def get_movie_url(content):
    soup = BeautifulSoup(content, "html.parser")
    movies = []
    for url in soup.find_all('a', class_="on_cover_link"):
        title = url.get("title")
        href = url.get("href")
        movies.append((title, href))
    return movies


# Iterating over movie archive and calling the get_url to grab urls
for page in tqdm(range(1,528)):
    page_address = "https://filmkio66.pw/movies/page/{}/".format(page)
    page_content = get(page_address).text
    download_queue = download_queue + get_movie_url(page_content)
    sleep(np.random.randint(5, 10))
    

# Saving movies urls so it can be used for futher use
df = pd.DataFrame(download_queue, columns =['Name', 'URL'])
df.to_csv(r"./kio_urls.csv", index=False)



movie_urls = pd.read_csv(r"./kio_urls.csv")


# Using urls csv file we now download the whole catalog
for index, row in tqdm(movie_urls.iterrows(), total=len(movie_urls)):
    if (index >= 7000) and (index < 8000):
        url = row["URL"]
        name = "".join(c for c in row["Name"] if c.isalpha() or c.isdigit() or c==' ').rstrip()
        page_content = get(url).text
        with open(r"./kio_raw/"+name+r".html", "w", encoding="utf-8") as page_descriptor:
            page_descriptor.write(page_content)
        sleep(np.random.randint(3, 6))