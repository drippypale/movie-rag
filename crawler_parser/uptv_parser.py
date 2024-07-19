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
specifically for UpTV and may not work on other websites.
"""


MOVIE_PATH = r"./uptv_raw"


# Using BeautifulSoup and reges, this function extracts the desired information
# It takes a soup object as an input which should be constructed using movie webpage
# Returns a tuple containing every usefull info from the webpage
def info_parser(soup):
    name = ""
    name_temp = soup.find('h1', class_="text-white h2 pb-lg-1 pb-md-1")
    if name_temp:
        name = name_temp.text
        name = re.sub(r"[آ-ی]", "", name).strip()

    imdb_score = ""
    imdb_temp = soup.find('div', class_="col-md-auto col-auto xs-p-0 ml-lg-30 ml-md-15")
    if imdb_temp:
        imdb_temp = soup.find('span', class_="font-weight-bold text-white small-15")
        if imdb_temp:
            imdb_score = imdb_temp.text.strip()

    genres = []
    genres_temp = soup.find('span', class_="d-inline-block category_post")
    if genres_temp:
        genres_temp = genres_temp.find_all('a')
        if genres_temp:
            genres = [x.text.strip() for x in genres_temp]
            genres = [x for x in genres if len(x)>0]
            
    
    release = ""
    if name:
        release_temp = re.search(r"(.*) (\d{4})", name)
        if release_temp:
            release = release_temp.group(2).strip()


    countries = ""
    countries_temp = soup.find('span', class_="d-md-inline-block d-none")
    if countries_temp:
        countries = countries_temp.text.strip()

    
    actors = []
    directors = []
    act_dic_temp = soup.find('div', class_="col-lg-12 col-md-12 d-md-block d-none col")
    if act_dic_temp:
        act_temp = act_dic_temp.find('div', class_="mb-half")
        dic_temp = act_dic_temp.find('div', class_="")
        if act_temp:
            act_temp = act_temp.find_all('a')
            actors = [x.text.strip() for x in act_temp]
        if dic_temp:
            dic_temp = dic_temp.find_all('a')
            directors = [x.text.strip() for x in dic_temp]
        

    story = ""
    story_temp = soup.find('p', class_="show-read-more")
    if story_temp:
        story = story_temp.text.strip()


    summ = ""
    summ_temp = soup.find('p', class_="show-read-more2")
    if summ_temp:
        summ = summ_temp.text.strip()


    idf = ""
    idf_temp = soup.find_all('a')
    for entry in idf_temp:
        url = entry.get('href')
        if url:
            if "imdb.com" in url:
                idf = url
        

    return (name, idf, imdb_score, genres, release, countries, directors, actors, story, summ)



# Gathering file names of DigiMovies webpages 
movie_names = [movie_file.name for movie_file in scandir(MOVIE_PATH)]
movie_info_parsed = []


# Iterate over files and extracting information
for movie in tqdm(movie_names, total=len(movie_names)):
    with open("/".join([MOVIE_PATH, movie]), encoding="utf-8") as file_descriptor:
        html_raw    = file_descriptor.read()

    soup = BeautifulSoup(html_raw, "html.parser")
    movie_info_parsed.append(info_parser(soup))


movies_df = pd.DataFrame(movie_info_parsed, columns=["name", "idf", "imdb_score", "genres", "release", "countries", "directors", "actors", "story", "summary"])
movies_df.to_csv(r"./uptv_movies.csv", index=False)
