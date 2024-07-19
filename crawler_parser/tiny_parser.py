from bs4 import BeautifulSoup
from os import scandir
import re
from tqdm import tqdm
import pandas as pd



"""
This file includes the code which parses and
extracts information from DigiMovies webpaes.
Every website uses different tags and classes for 
categorizing information, this code here was written 
specifically for TinyMovies and may not work on other websites.
"""


MOVIE_PATH = r"./tiny_raw"


# Using BeautifulSoup and reges, this function extracts the desired information
# It takes a soup object as an input which should be constructed using movie webpage
# Returns a tuple containing every usefull info from the webpage
def info_parser(movie_info, name, soup):
    imdb_score = ""
    crit_score = ""
    genres = []
    release = ""
    country = []
    language = []
    director = []
    actors = []
    summ = ""

    idf = ""
    idf_temp = soup.find('a', class_="fm-box-imdb")
    if idf_temp:
        idf = idf_temp.get('href')

    # Note that the tiny movies page structure lacked the proper tags
    # and classed so I had to the the text for identifying data
    for section in movie_info:
        text = section.text
        if "میانگین" in text:
            imdb_score = section.find('div', class_="imdb-rating ml-1").find('span').text
        elif "نمره منتقدین" in text:
            crit_score = section.find('span', class_="text-dark").text
        elif "ژانر" in text:
            genres = [y.text for y in section.find_all('a')]
        elif "سال انتشار" in text:
            release = re.sub("[آ-ی]", "", section.text).strip()
        elif "محصول" in text:
            country = [y.text for y in section.find_all('a', rel=True)]
        elif "زبان" in text:
            language = [y.text for y in section.find_all('a', rel=True)]
        elif "کارگردان" in text:
            director = [y.text for y in section.find_all('a', rel=True)]
        elif "بازیگران" in text:
            actors = [y.text for y in section.find_all('a', rel=True)]
        elif "خلاصه داستان:" in text:
            summ = re.sub("خلاصه داستان:", "", section.text)
                
                
    return (name, idf, imdb_score, crit_score, genres, release, country, language, director, actors, summ)



# Gathering file names of DigiMovies webpages 
movie_names = [movie_file.name for movie_file in scandir(MOVIE_PATH)]
movie_info_parsed = []


# Iterate over files and extracting information
for movie in tqdm(movie_names, total=len(movie_names)):
    with open("/".join([MOVIE_PATH, movie]), encoding="utf-8") as file_descriptor:
        html_raw    = file_descriptor.read()

    soup = BeautifulSoup(html_raw, "html.parser")
    movie_info = soup.find_all('li', class_="fm-infos")
    movie_info_parsed.append(info_parser(movie_info, movie.strip(r".html"), soup))


movies_df = pd.DataFrame(movie_info_parsed, columns=["name", "idf", "imdb_score", "crit_score", "genres", "release", "country", "language", "director", "actors", "summ"])
movies_df.to_csv(r"./tiny_movies.csv", index=False)