from bs4 import BeautifulSoup
from os import scandir
import re
from tqdm import tqdm
import pandas as pd
import json


"""
This file includes the code which parses and
extracts information from DigiMovies webpaes.
Every website uses different tags and classes for 
categorizing information, this code here was written 
specifically for DigiMovies and may not work on other websites.
"""


MOVIE_PATH = r"./digi_raw"

# Using BeautifulSoup and reges, this function extracts the desired information
# It takes a soup object as an input which should be constructed using movie webpage
# Returns a tuple containing every usefull info from the webpage
def info_parser(soup):
    name = ""
    release = ""
    name_temp = soup.find('title')
    if name_temp:
        name_temp = re.sub(r"[آ-ی]|\-", "", name_temp.text).strip()
        name = name_temp
        name_temp = re.search(r"(.*)(\d{4})", name_temp)
        if name_temp:
            release = name_temp.group(2).strip()

    imdb_score = ""
    imdb_temp = soup.find('strong', class_="greencol")
    if imdb_temp:
        imdb_score = imdb_temp.text.strip()


    crit_score = ""
    crit_temp = soup.find('strong', class_="greenlab")
    if crit_temp:
        crit_score = crit_temp.text.strip()


    genres = []
    genres_temp = soup.find_all('a')
    if genres_temp:
        for entry in genres_temp:
            url = entry.get("href")
            if url:
                if "genre" in url:
                    if "دانلود" not in entry.text:
                        genres.append(entry.text.strip())
            


    directors = []
    directors_temp = soup.find_all('a')
    if directors_temp:
        for entry in directors_temp:
            url = entry.get("href")
            if url:
                if "director" in url:
                    directors.append(entry.text.strip())


    actors = []
    ators_temp = soup.find_all('a')
    if ators_temp:
        for entry in ators_temp:
            url = entry.get("href")
            if url:
                if "actor" in url:
                    actors.append(entry.text.strip())


    countries = []
    countries_temp = soup.find_all('a')
    if countries_temp:
        for entry in countries_temp:
            url = entry.get("href")
            if url:
                if "country" in url:
                    countries.append(entry.text.strip())


    summ = ""
    summ_temp = soup.find('div', class_="plot_text")
    if summ_temp:
        summ = summ_temp.text.strip()

    idf = ""
    imdb_temp = soup.find('a', class_="imdb_icon_holder")
    if imdb_temp:
        idf = imdb_temp.get('href')
    

    return (name, idf, imdb_score, genres, release, countries, directors, actors, summ)



# Gathering file names of DigiMovies webpages 
movie_names = [movie_file.name for movie_file in scandir(MOVIE_PATH)]
movie_info_parsed = []


# Iterate over files and extracting information
for movie in tqdm(movie_names, total=len(movie_names)):
    with open("/".join([MOVIE_PATH, movie]), encoding="utf-8") as file_descriptor:
        html_raw    = file_descriptor.read()

    soup = BeautifulSoup(html_raw, "html.parser")
    movie_info_parsed.append(info_parser(soup))


movies_df = pd.DataFrame(movie_info_parsed, columns=["name", "idf", "imdb_score", "genres", "release", "countries", "directors", "actors", "summary"])
movies_df.to_csv(r"./digi_movies.csv", index=False)

