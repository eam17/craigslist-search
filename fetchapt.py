# Gets the page source using  HTTP request
from requests import get

# Parses HTML
from bs4 import BeautifulSoup


# Get a list of posts currently on the page
def find_posts(url):
    found_posts = {}
    response = get(url)
    # Get the source code of the page
    html_soup = BeautifulSoup(response.text, 'html.parser')
    # Get the macro-container for the posts
    posts = html_soup.find_all('li', class_='result-row')
    # Parse each post into id, href and title
    for post in posts:
        post_title = post.find('a', class_='result-title hdrlnk')
        post_title_id = int(post_title['data-id'])
        post_title_text = post_title.text
        post_link = post_title['href']
        post_hood = post.find('span', class_='result-hood')
        if post_hood is None:
            post_hood = ""
        else:
            post_hood = post_hood.text
        item = [str(post_title_text), str(post_link), post_hood]
        found_posts[post_title_id] = item
    # Return a dictionary of post ids mapped to href and title
    return found_posts.copy()


# Returns a tuple of lat and lon from the post at url
def find_lat_lon(url):
    response = get(url)
    # Get the source code of the page
    post = BeautifulSoup(response.text, 'html.parser')

    # Get the lat and lon of the post
    geo = post.find("meta", attrs={'name': 'geo.position'})['content']
    geo = geo.split(';')
    lat = geo[0]
    lon = geo[1]
    return tuple((lat, lon))


def test():
    # find_posts('https://denver.craigslist.org/search/zip?')
    url = 'https://denver.craigslist.org/zip/d/aurora-bike-ramps/7234476118.html'
    find_lat_lon(url)


# test()
