from bs4 import BeautifulSoup
from time import sleep
from random import randint
from selenium import webdriver
browserpath = ""
driver_path="C:/Users/chloe/OneDrive/Desktop/selenium.exe"

wd = webdriver.Chrome(executable_path=driver_path)
workids = []
links = []

def TestSearch(keyterm):
    wd.get("https://archiveofourown.org/works/search?utf8=%E2%9C%93&work_search%5Bquery%5D=" + keyterm + "&work_search%5Btitle%5D=&work_search%5Bcreators%5D=&work_search%5Brevised_at%5D=&work_search%5Bcomplete%5D=&work_search%5Bcrossover%5D=&work_search%5Bsingle_chapter%5D=0&work_search%5Bword_count%5D=&work_search%5Blanguage_id%5D=en&work_search%5Bfandom_names%5D=&work_search%5Brating_ids%5D=11&work_search%5Bcharacter_names%5D=&work_search%5Brelationship_names%5D=&work_search%5Bfreeform_names%5D=&work_search%5Bhits%5D=&work_search%5Bkudos_count%5D=&work_search%5Bcomments_count%5D=&work_search%5Bbookmarks_count%5D=&work_search%5Bsort_column%5D=hits&work_search%5Bsort_direction%5D=desc&commit=Search")
    sleep(3)
    tosbutton = wd.find_element_by_id("tos_agree")
    tosbutton.click()
    accept_tos = wd.find_element_by_id("accept_tos")
    accept_tos.click()

def ScrapeWorkIDs(keyterm,pages):
    for x in range(1, pages):
        wd.get("https://archiveofourown.org/works/search?commit=Search&page=" + str(x) + "&utf8=%E2%9C%93&work_search%5Bbookmarks_count%5D=&work_search%5Bcharacter_names%5D=&work_search%5Bcomments_count%5D=&work_search%5Bcomplete%5D=&work_search%5Bcreators%5D=&work_search%5Bcrossover%5D=&work_search%5Bfandom_names%5D=&work_search%5Bfreeform_names%5D=&work_search%5Bhits%5D=&work_search%5Bkudos_count%5D=&work_search%5Blanguage_id%5D=en&work_search%5Bquery%5D=" + keyterm + "&work_search%5Brating_ids%5D=11&work_search%5Brelationship_names%5D=&work_search%5Brevised_at%5D=&work_search%5Bsingle_chapter%5D=0&work_search%5Bsort_column%5D=hits&work_search%5Bsort_direction%5D=desc&work_search%5Btitle%5D=&work_search%5Bword_count%5D=")
        data = wd.page_source
        soup = BeautifulSoup(data, 'html.parser')
        div_tags = soup.find_all(role='article')
        for div in div_tags:
             ID = div.get('id')
             if ID is not None:
                 workids.append(ID)

def CleanIDs(s):
    return s[5:]

def GetPDFLinks(workids):
    workids = [CleanIDs(s) for s in workids]
    for ID in workids:
        wd.get("https://archiveofourown.org/works/" + ID)
        data = wd.page_source
        soup = BeautifulSoup(data, 'html.parser')
        link = soup.find("a",string="PDF")
        links.append(link.get('href'))
    print(links)

def DownloadPDFs(links):
    for link in links:
        wd.get("https://archiveofourown.org"+link)
        sleep(1)

def Main():
    keyterm = input("Please input your search term")
    pages = int(input("Please input number of pages to scrape"))
    TestSearch(keyterm)
    ScrapeWorkIDs(keyterm,pages)
    GetPDFLinks(workids)
    DownloadPDFs(links)

Main()
