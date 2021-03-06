#!/usr/bin/env python
# Name:
# Student number:
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

    # ADD YOUR CODE HERE TO EXTRACT THE ABOVE INFORMATION ABOUT THE
    # HIGHEST RATED MOVIES
    # NOTE: FOR THIS EXERCISE YOU ARE ALLOWED (BUT NOT REQUIRED) TO IGNORE
    # UNICODE CHARACTERS AND SIMPLY LEAVE THEM OUT OF THE OUTPUT.

    # TARGET_URL = "https://www.imdb.com/search/title?title_type=feature&release_date=2008-01-01,2018-01-01&num_votes=5000,&sort=user_rating,desc"
    #
    # # opening up connection grabbing the page
    # uClient = uReq(TARGET_URL)
    # page_html = uClient.read()
    # uClient.close()
    #
    # # HTML parsing
    # page_soup = BeautifulSoup(page_html, 'html.parser')

    # grabs each product
    containers = dom.findAll("div",{"class":"lister-item-content"})

    # filename = "movies.csv"
    # f = open(filename, "w")
    # headers = "Title, Rating, Year, Actors, Runtime\n"
    # f.write(headers)

    for container in containers:
        # container = containers[0]
        actors_list = []

        title_container = container.findAll("a")[0]
        title_movie = title_container.text
        rating_container = container.findAll("strong")[0]
        rating_movie = rating_container.text
        year_container = container.findAll("span")[1]
        year_movie = year_container.text
        for actors in container.findAll("a", attrs={"href": re.compile("/?ref_=adv_li_st_")}):
            actors_movie = actors.text
            actors_list.append(actors_movie)
            actors_string = ", ".join(actors_list)
        # print(actors_string)
        runtime_container = container.findAll("span", {"class":"runtime"})
        runtime_movie = runtime_container[0].text
        print("title_movie: " + title_movie)
        print("rating_movie: " + rating_movie)
        print("year_movie: " + year_movie)
        print("actors_string: " + actors_string)
        print("runtime_movie: " + runtime_movie)
        print()


        # f.write(title_movie + "," + rating_movie + "," + year_movie + "," + actors_string + "," + runtime_movie + "\n")

    f.close()

def save_csv(outfile, movies):
    """
    Output a CSV file containing highest rated movies.
    """
    writer = csv.writer(outfile)
    writer.writerow(['Title', 'Rating', 'Year', 'Actors', 'Runtime'])

    # ADD SOME CODE OF YOURSELF HERE TO WRITE THE MOVIES TO DISK


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
