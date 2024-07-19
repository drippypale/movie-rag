import pandas as pd
from requests import get
from bs4 import BeautifulSoup
from tqdm import tqdm
import re
from time import sleep
import numpy as np

"""
After crawling and parsing the data form iranian
websites, we meeded a form of validation for our proposed method.
Using movie ids which has been extracted from aforementioned wesites
I downloaded the movie pages from imdb and extracted the "similar movies" section
"""

data_set = pd.read_csv(r"./final_dataset.csv")

# The imdb was sensitive to answering generic requests so I had ti modify the 
# requests heads to get a proper response instead of 405 code
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}


# Here I constructed imdb urls using movie ids and downloaded the pages for further use
for index, row in tqdm(data_set.iterrows(), total=len(data_set)):
    if (index > 8000) and (index <= 8400):
        url = "https://www.imdb.com/title/" + str(row["idf"]) + "/"
        content = get(url, headers=headers).text
        with open(r"./imdb/{}.html".format(row["idf"]), 'w', encoding="utf-8") as file_dsc:
            file_dsc.write(content)
        sleep(np.random.randint(3, 6))
    



data_set = pd.read_csv(r"./final_dataset.csv")
data_set_sim = data_set.assign(similar_movies=[[] for  x in range(len(data_set))])

# Iteraring over the downloaded pages and extracting "similar movies" section
for index, row in tqdm(data_set_sim.iterrows(), total=len(data_set_sim)):
    file_path = "./imdb/" + row["idf"] + ".html"
    with open(file_path, 'r', encoding="utf-8") as file_dsc:
        contents = file_dsc.read()

    soup = BeautifulSoup(contents, "html.parser")
    similars_temp = soup.find_all('a', class_="ipc-poster-card__title ipc-poster-card__title--clamp-2 ipc-poster-card__title--clickable")
    if similars_temp:
        for item in similars_temp:
            row["similar_movies"].append((item.text, re.search(r"/title/(tt\d+)/", item.get("href")).group(1)))


# save the result
data_set_sim.to_csv(r"movie_data_set.csv", index=False)

    