import csv
from sys import maxsize
import pandas as pd
import matplotlib.pyplot as plt
import folium
from folium import IFrame

df = pd.read_csv('result.csv')
# print(df)

threshold = .01
home = [['Home'], [39.7190608], [-104.8170952]]


# distance sq (easy to compute)
def findDistSquared(lat1, long1, lat2, long2):
    return (lat1 - lat2) ** 2 + (long1 - long2) ** 2


# distance sq (easy to compute)
def findDistFromHome(row):
    home_lat = 39.7190608
    home_long = -104.8170952
    return ((row['Latitude'] - home_lat) ** 2 + (row['Longitude'] - home_long) ** 2) < threshold


# opposite of above, not a great way to do this tbh
def findDistFromHome2(row):
    home_lat = 39.7190608
    home_long = -104.8170952
    return ((row['Latitude'] - home_lat) ** 2 + (row['Longitude'] - home_long) ** 2) >= threshold


close = df.apply(findDistFromHome, axis=1)
notclose = df.apply(findDistFromHome2, axis=1)
df2 = df[notclose]
df = df[close]

df = df.reset_index(drop=True)
print(df)

df.iloc[0] = ["", 39.7190608, -104.8170952]

dist = [[0] * len(df.index)] * len(df.index)
mini = 10
maxi = 0

for x in df.index:
    for y in df.index:
        num = findDistSquared(df['Latitude'][x], df['Longitude'][x], df['Latitude'][y], df['Longitude'][y])

        if mini > num != 0:
            mini = num

        if maxi < num:
            maxi = num

        if num < threshold:
            dist[x][y] = num
print(dist)
print(mini)
print(maxi)

cities = [['Aurora', 'Denver', 'Thornton', 'Westminster', 'Centennial', 'Englewood', 'Parker'],
          [39.6887504, 39.7642543, 39.9156658, 39.8933109, 39.6022184, 39.6476682, 39.5080343],
          [-104.8272602, -104.9955381, -105.0200119, -105.1468057, -104.927733, -105.0322957, -104.8359005]]

# print(travellingSalesmanProblem(dist, 0))
for a in range(len(df.index)):
    print(str(a) + ": " + str(df['URL'][a]))

plt.plot(df['Longitude'], df['Latitude'], 'ro')
plt.plot(df2['Longitude'], df2['Latitude'], 'bs')
plt.plot(cities[2], cities[1], 'g^')
plt.plot(home[2], home[1], 'gs')
plt.axis([-105.5, -104.5, 39.2, 40.2])
# plt.show()

my_map4 = folium.Map(location=[home[1][0], home[2][0]], zoom_start=12)


def getHref(url):

    html = """
        <a href="{url}" target="_blank">{url}</a>
        """.format(url=url)
    iframe = IFrame(html=html, width=300, height=100)
    popup = folium.Popup(iframe, max_width=2650)
    return popup


for a in range(len(df.index)):
    print(str(a) + ": " + str(df['URL'][a]) + ": " + str(df['Latitude'][a]) + ": " + str(df['Longitude'][a]))
    folium.Marker([df['Latitude'][a], df['Longitude'][a]], popup=getHref(df['URL'][a])).add_to(my_map4)

# Add a line to the map by using line method .
# it connect both coordiates by the line
#fig, ax = plt.subplots(figsize=(width, height))
#ax = df.plot(ax=ax, legend=False)

# line_opacity implies intensity of the line


my_map4.save("my_map4.html")


