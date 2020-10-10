# import get to call a get request on the site
from requests import get

import re


from bs4 import BeautifulSoup




found_posts = {}


def find_posts():
    response = get(
        'https://denver.craigslist.org/search/zip?')
    html_soup = BeautifulSoup(response.text, 'html.parser')
    # get the macro-container for the posts
    posts = html_soup.find_all('li', class_='result-row')
    found_posts_arr = []
    for post in posts:
        post_title = post.find('a', class_='result-title hdrlnk')
        post_title_id = post_title['data-id']
        post_title_text = post_title.text
        post_link = post_title['href']
        item = [post_title_text, post_link]
        found_posts[post_title_id] = item
        found_posts_arr.append(post)
    return found_posts_arr.copy()

#print(type(posts))  # to double check that I got a ResultSet
#print(len(posts))  # to double check I got 120 (elements/page)

#found_posts_key = {}


def find_posts_key(keyarray, url):
    response = get('https://denver.craigslist.org/search/zip?')
    print("got response")
    html_soup = BeautifulSoup(response.text, 'html.parser')
    # get the macro-container for the posts
    posts = html_soup.find_all('li', class_='result-row')
    found_posts_key_arr = []
    for post in posts:
        post_title = post.find('a', class_='result-title hdrlnk').text
        post_title_lst = convert(post_title)
        for keyword in keyarray:
            if keyword in post_title_lst:
                found_posts_key_arr.append(post)
    return found_posts_key_arr.copy()


def convert(lst):
    lst = lst.split()
    resultList = []
    for l in lst:
        resultList.append(l.lower())
    return resultList


def find_posts_key_r(keyarray, url):
    response = get('https://williamsport.craigslist.org/search/zip?')
    print("got response")
    html_soup = BeautifulSoup(response.text, 'html.parser')
    # get the macro-container for the posts
    posts = html_soup.find_all('li', class_='result-row')
    found_posts_key_arr = []
    for post in posts:
        post_title = post.find('a', class_='result-title hdrlnk').text
        post_title_lst = convert(post_title)
        for keyword in keyarray:
            if keyword in post_title_lst:
                found_posts_key_arr.append(post)
    return found_posts_key_arr.copy()


url = 'https://denver.craigslist.org/search/zip?'

def test_find_posts(urlKey):
    response = get(urlKey)
    # print("got response")
    html_soup = BeautifulSoup(response.text, 'html.parser')
    # get the macro-container for the posts
    posts = html_soup.find_all('li', class_='result-row')
    #print(posts[0])
    post_title = posts[0].find('a', class_='result-title hdrlnk').text
    post_price = posts[0].find('span', class_='result-price').text
    post_hood = posts[0].find('span', class_='result-hood').text
    print(post_title)
    print(post_hood)
    post_price = re.sub('[!@#$]', '', post_price)
    print(int(post_price))


test_find_posts(url)