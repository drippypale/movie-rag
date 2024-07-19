from requests import get
from bs4 import BeautifulSoup
import re
import pandas as pd
from time import sleep
from tqdm import tqdm


"""
This file includes the code which crawls and
downloads movie pages from TinyMovies website.
"""


download_queue = []


# This function find the selects the movie url from the given page
# It has been customized for TinyMovies webpages
def get_movie_url(content):
    soup = BeautifulSoup(content, "html.parser")
    movies = []
    for url in soup.find_all('a', class_="read-more-link btn btn-outline-danger"):
        title = re.sub(r"[آ-ی]", "", url.get("title")).strip()
        href = url.get("href")
        movies.append((title, href))
    return movies


# Iterating over movie archive and calling the get_url to grab urls
for page in tqdm(range(1,363)):
    page_address = "https://2tinymov.site/category/%d8%af%d9%88%d8%a8%d9%84%d9%87-%d9%87%d8%a7-%d8%b3%d8%a7%db%8c%d8%aa/page/{}/".format(page)
    page_content = get(page_address).text
    download_queue = download_queue + get_movie_url(page_content)
    sleep(2)
    

# Saving movies urls so it can be used for futher use
df = pd.DataFrame(download_queue, columns =['Name', 'URL'])
df.to_csv(r"./movie_translated_urls.csv", index=False)


movie_urls = pd.read_csv(r"./movie_translated_urls.csv")


# Using urls csv file we now download the whole catalog
for index, row in tqdm(movie_urls.iterrows(), total=len(movie_urls)):
    url = row["URL"]
    name = "".join(c for c in row["Name"] if c.isalpha() or c.isdigit() or c==' ').rstrip()
    page_content = get(url).text
    with open(r"./tiny_translated_raw/"+name+r".html", "w", encoding="utf-8") as page_descriptor:
        page_descriptor.write(page_content)
    sleep(2)