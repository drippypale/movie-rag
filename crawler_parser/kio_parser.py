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
specifically for FilmKio and may not work on other websites.
"""


MOVIE_PATH = r"./kio_raw"


# Using BeautifulSoup and reges, this function extracts the desired information
# It takes a soup object as an input which should be constructed using movie webpage
# Returns a tuple containing every usefull info from the webpage
def info_parser(soup):
    name_temp = soup.find('div', class_="right_side_meta")
    if name_temp:
        name_temp = name_temp.find('h1')
        if name_temp:
            name_temp = re.sub(r"[آ-ی]", "",name_temp.text, ).strip()
    else:
        name_temp = ""

    name_re = re.search(r"(.*) \d{4}", name_temp) if len(name_temp) > 0 else ""
    name = name_re.group(1) if name_re else ""

    name_fa = soup.find('div', class_="right_side_meta")
    if name_fa:
        name_fa = name_fa.find('h2')
        if name_fa:
            name_fa = name_fa.text.strip()
    else:
        name_fa = ""



    release_re = re.search(r".* (\d{4})", name_temp) if len(name_temp) > 0 else ""
    release = release_re.group(1) if release_re else ""

    imdb_score = soup.find('div', class_="imdb_rate_single")
    if imdb_score:
        imdb_score = imdb_score.find('div', class_="rate_average_num")
        if imdb_score:
            imdb_score = imdb_score.text.strip()
    else:
        imdb_score = ""


    directors_find = soup.find('div', class_="row_cast directors")
    directors = []
    if directors_find:
        directors = [x.text for x in directors_find.find_all('a')]
    
    countries_find = soup.find('div', class_="row_cast country")
    countries = []
    if countries_find:
        countries = [x.text for x in countries_find.find_all('a')]

    genres_find = soup.find('div', class_="genre_list")
    genres = []
    if genres_find:
        genres = [x.text for x in genres_find.find_all('a')]
    
    actors_find = soup.find('div', class_="row_more_data_slider cast_list")
    actors = []
    if actors_find:
        actors = [x.text for x in actors_find.find('div', "body_slider_data_single").find_all('h3')]

    stars_find = soup.find('div', class_="row_cast stars")
    stars = []
    if stars_find:
        stars = [x.text for x in stars_find.find_all('a')]

    summ = soup.find('div', "presentation").text.strip() if soup.find('div', "presentation") else ""

    more_data = soup.find('ul', class_="more_data_single")
    languages = []
    crit_score = ""
    tomt_score = ""
    authors = []
    # This part here didn't have proper tags so I had to use the text itself
    if more_data:
        for entry in more_data:
            text =  entry.text
            if "زبان" in text:
                languages = text.split(":")[1].strip().split(",")
            elif "امتیاز منتقدین" in text:
                crit_score = text.split(":")[1].strip()
            elif "راتن تومیتوز" in text:
                tomt_score = text.split(":")[1].strip()
            elif "نویسنده" in text:
                authors = text.split(":")[1].strip().split(",")


    idf = ""
    idf_temp = soup.find('a', class_="imdbLinkIcon")
    if idf_temp:
        idf = idf_temp.get("href")


    return (name, idf, name_fa, imdb_score, crit_score, tomt_score, genres, release, countries, languages, directors, authors, stars, actors, summ)


# Gathering file names of DigiMovies webpages 
movie_names = [movie_file.name for movie_file in scandir(MOVIE_PATH)]
movie_info_parsed = []


# Iterate over files and extracting information
for movie in tqdm(movie_names, total=len(movie_names)):
    with open("/".join([MOVIE_PATH, movie]), encoding="utf-8") as file_descriptor:
        html_raw    = file_descriptor.read()

    soup = BeautifulSoup(html_raw, "html.parser")
    movie_info_parsed.append(info_parser(soup))


movies_df = pd.DataFrame(movie_info_parsed, columns=["name", "idf", "name_fa", "imdb_score", "crit_score", "tomato_score", "genres", "release", "countries", "languages", "directors", "authors", "stars", "actors", "summary"])
movies_df.to_csv(r"./kio_movies.csv", index=False)
