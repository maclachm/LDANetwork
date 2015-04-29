__author__ = 'maclachm'
import urllib2, re, json

def getDoc(name):
    #Wikipedia API

    baseUrl = "http://en.wikipedia.org/w/api.php?format=json&action=" \
          "query&titles="
    NameUrl = baseUrl + name.replace(' ', '_').replace('\n', '') + "&prop=extracts"

    text =  json.loads(urllib2.urlopen(NameUrl).read())
    print text
    text = re.sub('[^0-9a-zA-Z]+', ' ', str(text['query']['pages']) )

    return text


with open("FamousPeople.txt") as n: #names file, format: First Last
    for line in n.readlines():
        title = line[0:len(line)-1]+'.txt'
        with open(title, 'w') as out:
            text = getDoc(line)
            out.write(text)



