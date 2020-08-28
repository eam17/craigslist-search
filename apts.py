# import get to call a get request on the site
from requests import get

# get the first page of the east bay housing prices


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


#def find_posts_key(keyword):
    ###for post in posts:
        #post_title = post.find('a', class_='result-title hdrlnk')
       # post_title_text = post_title.text
       # if keyword in post_title_text:
        #    post_title_id = post_title['data-id']
       #     found_posts_key[post_title_id] = post
 #   return found_posts_key