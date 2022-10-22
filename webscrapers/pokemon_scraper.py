from bs4 import BeautifulSoup
import requests
import html5lib

directory = r"C:\Users\chloe\OneDrive\Desktop\sprites"

def SetUp():
    URL = "https://pokemondb.net/pokedex/national"
    full_html = requests.get(URL).content
    soup = BeautifulSoup(full_html, 'html.parser')
    return soup

def GetLinks(soup):
    links = []
    names = []
    for link in soup.find_all('span', attrs={'class': 'img-fixed img-sprite'}):
        links.append(link['data-src'])
        names.append(link['data-alt'])
    return links, names

def MakeFilenames(names):
    filenames = []
    for name in names:
        back = directory + "\\" + name + '.jpg'
        filenames.append(back)
    return filenames

def DownloadLink(input):
    link, filename = input[0], input[1]
    try:
        r = requests.get(link)
        with open(filename, 'wb') as f:
            f.write(r.content)
        print("Downloaded:", filename)
        return(link)
    except Exception as e:
        print('Exception in download_url():',e)

def DownloadLinks(input):
    for i in inputs:
        result = DownloadLink(i)

soup = SetUp()
links, names = GetLinks(soup)
filenames = MakeFilenames(names)
inputs = zip(links, filenames)
DownloadLinks(inputs)
