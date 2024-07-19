from requests import get
from bs4 import BeautifulSoup
import re
import pandas as pd
from time import sleep
from tqdm import tqdm
import numpy as np


"""
This file includes the code which crawls and
downloads movie pages from DigiMovies website.
"""


download_queue = []


# This function find the selects the movie url from the given page
# It has been customized for DigiMovies webpages
def get_movie_url(content):
    soup = BeautifulSoup(content, "html.parser")
    movies = []
    for url in soup.find_all('h1', class_="h5 d-inline-block"):
        temp = url.find('a')
        title = temp.get("title")
        href = temp.get("href")
        movies.append((title, href))
    return movies



# Iterating over movie archive and calling the get_url to grab urls
for page in tqdm(range(1,384)):
    page_address = "https://www.uptvs.com/category/moviesz/page/{}".format(page)
    page_content = get(page_address).text
    download_queue = download_queue + get_movie_url(page_content)
    sleep(np.random.randint(3, 6))
    

df = pd.DataFrame(download_queue, columns =['Name', 'URL'])
df.to_csv(r"./uptv_urls.csv", index=False)





movie_urls = pd.read_csv(r"./uptv_urls.csv")

# Using urls csv file we now download the whole catalog
for index, row in tqdm(movie_urls.iterrows(), total=len(movie_urls)):
    if index >= 4000:
        url = row["URL"]
        name = "".join(c for c in row["Name"] if c.isalpha() or c.isdigit() or c==' ').rstrip()
        page_content = get(url).text
        with open(r"./uptv_raw/"+name+r".html", "w", encoding="utf-8") as page_descriptor:
            page_descriptor.write(page_content)
        sleep(np.random.randint(3, 6))