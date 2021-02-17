import sqlite3

# Datetime for DB
import datetime

# Returns a list of posts on the page
import fetchapt

# Contains functions that have to do with distance in latitudes and longitudes
import geolocator


# c.execute("INSERT INTO posts VALUES (1,'https://testing','Title with many cool word in it', ?)", (time,))

# conn.commit()

# add filtering by money, location, use the main denver page url
# location first
#


def add_new_posts_to_db(url, key_array):
    # Fetch the data on the page
    posts_found = fetchapt.find_posts(url)
    print("Posts fetched - ", len(posts_found))
    # Filter out the posts without key words
    posts_found = filter_posts(posts_found, key_array)
    print("posts_found: ", posts_found)
    # go through each post, look at id. if id isn't in DB, add it, href, title, and time added
    for post_id in posts_found:
        conn = sqlite3.connect('craigslistDB.db')
        c = conn.cursor()
        print("post_id: ", post_id)
        result = c.execute('SELECT * FROM posts WHERE post_id =?', (post_id,)).fetchall()
        row_count = len(result)
        if row_count == 1:
            # Post already in the DB, nothing to do
            break
        elif row_count == 0:
            # No rows with this id
            time = datetime.datetime.now()
            print("time: ", time, "post_id:  ", post_id, "posts_found: ", posts_found)
            post = posts_found[post_id]
            # Id, href, title, area, timeadded
            c.execute('INSERT INTO posts VALUES (?,?,?,?,?)', (post_id, post[1], post[0], post[2], time))
            print("Post added")
        else:
            print("id is either in or not in the DB, this shouldn't be happening!")
        conn.commit()
        conn.close()


# c = sqlite3.connect('craigslistDB.db').cursor()
# for row in c.execute('SELECT * FROM posts'):
#     print(row)


# Returns a list of tuples containing titles, hrefs and area that are new since the last check
def check_for_new_posts(url, old_time, key_array):
    add_new_posts_to_db(url, key_array)
    conn = sqlite3.connect('craigslistDB.db')
    c = conn.cursor()
    new_posts = []
    # Grab posts whose time is bigger than old_time
    for row in c.execute('SELECT * FROM posts WHERE timeadded >? ORDER BY timeadded DESC', (old_time,)).fetchall():
        item = (row[1], row[2], row[3])
        # print(item)
        new_posts.append(item)
    conn.close()
    # Returns a list of tuples containing new post details
    return new_posts.copy()


# Converts a string of words into an array of lowercase strings
def convert(title_list):
    title_list = title_list.split()
    result_list = []
    for word in title_list:
        result_list.append(word.lower())
    return result_list


# Accepts a dict, returns a dict of posts only containing provided keywords
def filter_posts(posts, filter_words):
    print("in filter", posts)
    filtered_posts = {}
    for post_id in posts:
        title = str(posts[post_id][0])
        title_arr = convert(title)
        for keyword in filter_words:
            if keyword in title_arr:
                # print("post_id: ", post_id)
                # print("posts[post_id]: ", posts[post_id])
                # how to add to dictionary?
                filtered_posts[post_id] = posts[post_id]
                # print("filter keeps: ", title)
    return filtered_posts.copy()


# Accepts a dict of posts, a string of home city name+state and an int of miles
# Returns a list of tuples containing titles, hrefs and areas only of those posts that are within *miles* of the *home_city*
def check_distance(posts, home_city, miles):
    new_posts = []
    for post_id in posts:
        print(posts[post_id])
        # get the href of the post
        href = posts[post_id][1]
        # get geo info of the post from the href
        away_city = fetchapt.find_lat_lon(href)
        if geolocator.is_within_miles(geolocator.point_for_city_state(home_city), away_city, miles):
            item = (posts[post_id][0], posts[post_id][1], posts[post_id][2])
            new_posts.append(item)
    return new_posts.copy()


def test():
    ol_time = '2020-11-15 17:50:36.495623'
    key_array = ["bike", "table", "ikea", "wood", "plane", "tool", "tools", "chisel", "chisels", "desk", "saw",
                 "weights"]
    url = 'https://denver.craigslist.org/search/zip?'
    # posts = check_for_new_posts(url, ol_time, key_array)
    posts = fetchapt.find_posts(url)
    posts = filter_posts(posts, key_array)
    print("before filter: ", len(posts))
    city1 = geolocator.point_for_city_state("aurora colorado")

    check_distance(posts, city1, 15)
    print("after filter: ", len(posts))

# test()

example = ('https://denver.craigslist.org/zip/d/arvada-loveseat-couch/7232209596.html', 'Loveseat couch', ' (arvada)')