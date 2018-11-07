from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

my_url = "https://www.imdb.com/search/title?title_type=feature&release_date=2008-01-01,2018-01-01&num_votes=5000,&sort=user_rating,desc"

# opening up connection grabbing the page
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

# HTML parsing
page_soup = soup(page_html, "html.parser")

# grabs each product
containers = page_soup.findAll("div",{"class":"lister-item-content"})

filename = "test.csv"
f = open(filename, "w")
headers = "name, number\n"
f.write(headers)

for container in containers:

    title_container = container.findAll("a", {"href":"/title/tt5963218/?ref_=adv_li_tt"})
    title_movie = title_container[0].text
    number_container = container.findAll("span", {"class":"lister-item-index unbold text-primary"})
    number_movie = number_container[0].text

    print("title_movie: " + title_movie)
    print("number_movie: " + number_movie)

    f.write(title_movie + "," +number_movie + "\n")

f.close()
