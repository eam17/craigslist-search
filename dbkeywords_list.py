import sqlite3


def add_new_keywords(key_array):
    conn = sqlite3.connect('craigslistDB.db')
    c = conn.cursor()
    for word in key_array:
        result = c.execute('SELECT * FROM keywords WHERE keyword =?', (word,)).fetchall()
        if len(result) <= 0:
            c.execute('INSERT INTO keywords VALUES (?)', (word,))
            print(word, " added")
            conn.commit()
        else:
            print(word, " already in the list")
    conn.close()


def remove_keywords(key_array):
    conn = sqlite3.connect('craigslistDB.db')
    c = conn.cursor()
    for word in key_array:
        result = c.execute('SELECT * FROM keywords WHERE keyword =?', (word,)).fetchall()
        if len(result) > 0:
            c.execute('DELETE FROM keywords WHERE keyword =?', (word,))
            print(word, " removed")
            conn.commit()
        else:
            print(word, " not in the list")
    conn.close()


# Returns an array of keywords in the table
def fetch_keywords():
    conn = sqlite3.connect('craigslistDB.db')
    c = conn.cursor()
    key_array = []
    result = c.execute('SELECT * FROM keywords').fetchall()
    if len(result) > 0:
        for row in result:
            item = "".join(row)
            key_array.append(item)
    else:
        print("Nothing in the list")
    conn.close()
    return key_array.copy()


def check_server_db(server):
    conn = sqlite3.connect('craigslistDB.db')
    c = conn.cursor()
    result = c.execute('SELECT * FROM server_info WHERE server_id =?', (server.id, )).fetchall()
    if len(result) < 1:
        # add the server id to the db
        c.execute('INSERT INTO server_info VALUES (?,null, null, null, null)', (server.id,))
        print("result")

    result = c.execute('SELECT * FROM server_info WHERE server_id =?', (server.id,)).fetchall()
    if len(result) < 1:
        print("Result shouldn't be empty!!")
    else:
        print(result)
    conn.commit()
    conn.close()


def test():
    # fetch_keywords()
    keywords_array = ["bike", "table", "ikea", "wood", "plane", "tool", "tools", "chisel", "chisels", "desk", "saw", "weights"]
    add_new_keywords(keywords_array)
    remove_keywords(["bike"])
    words = fetch_keywords()
    for word in words:
        print(word)


# test()