import nltk
def convert(lst):
    lst = lst.split()
    resultList = []
    for l in lst:
        resultList.append(l.lower())
    return resultList
text = "Curb alert FREE Floral pull out couch/sleeper queen size"
print(convert(text))