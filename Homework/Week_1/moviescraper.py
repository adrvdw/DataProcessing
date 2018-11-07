#!/usr/bin/env python
# Name: Ad Ruigrok van der Werve
# Student number: 11323760
"""
This script scrapes IMDB and outputs a CSV file with highest rated movies.
"""
import re
import csv
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup # as Soup
from urllib.request import urlopen as uReq

TARGET_URL = "https://www.imdb.com/search/title?title_type=feature&release_date=2008-01-01,2018-01-01&num_votes=5000,&sort=user_rating,desc"
BACKUP_HTML = 'movies.html'
OUTPUT_CSV = 'movies.csv'


def extract_movies(dom):
    """
    Extract a list of highest rated movies from DOM (of IMDB page).
    Each movie entry should contain the following fields:
    - Title
    - Rating
    - Year of release (only a number!)
    - Actors/actresses (comma separated if more than one)
    - Runtime (only a number!)
    """

    containers = dom.findAll("div",{"class":"lister-item-content"})

    movies = []

    for container in containers:
        # container = containers[0]
        actors_list = []
        year_movie_list = []

        # find specific elements and extract from HTML page
        title_container = container.findAll("a")[0]
        title_movie = title_container.text

        rating_container = container.findAll("strong")[0]
        rating_movie = rating_container.text

        year_container = container.findAll("span")[1]
        year_movie = year_container.text
        year_movie_list.append(year_movie)
        year_movie = year_movie.replace("(", "")
        year_movie = year_movie.replace(")", "")
        year_movie = year_movie.replace("I", "")
        year_movie = year_movie.replace(" ", "")

        for actors in container.findAll("a", attrs={"href": re.compile("/?ref_=adv_li_st_")}):
            actors_movie = actors.text
            actors_list.append(actors_movie)
            actors_string = ", ".join(actors_list)

        runtime_container = container.findAll("span", {"class":"runtime"})
        runtime_movie = runtime_container[0].text
        runtime_movie = runtime_movie.replace("min", "")
        runtime_movie = runtime_movie.replace(" ", "")
        # add information to created list
        movies.append(title_movie)
        movies.append(rating_movie)
        movies.append(year_movie)
        movies.append(actors_string)
        movies.append(runtime_movie)

    return(movies)

def save_csv(outfile, movies):
    """
    Output a CSV file containing highest rated movies.
    """
    writer = csv.writer(outfile)
    writer.writerow(['Title', 'Rating', 'Year', 'Actors', 'Runtime'])

    list = []

    counter = 0
    for i in movies:
        # every seventh element is the start of a new movie
        if counter % 5 == 0 and counter != 0:
            number_end = int(counter + 5)
            number_begin = int(counter)
            info_movie = movies[number_begin:number_end]
            list.append(info_movie)
            writer.writerow(info_movie)
        counter += 1

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        print('The following error occurred during HTTP GET request to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns true if the response seems to be HTML, false otherwise
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


if __name__ == "__main__":

    # get HTML content at target URL
    html = simple_get(TARGET_URL)

    # save a copy to disk in the current directory, this serves as an backup
    # of the original HTML, will be used in grading.
    with open(BACKUP_HTML, 'wb') as f:
        f.write(html)

    # parse the HTML file into a DOM representation
    dom = BeautifulSoup(html, 'html.parser')

    # extract the movies (using the function you implemented)
    movies = extract_movies(dom)

    # write the CSV file to disk (including a header)
    with open(OUTPUT_CSV, 'w', newline='') as output_file:
        save_csv(output_file, movies)
