from selenium import webdriver
import time
import requests
import os
from PIL import Image
import io
import hashlib

driver_Path = "C:/Users/chloe/OneDrive/Desktop/chromedriver.exe"

def scroll_To_End(wd, sleep_length):
    wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(sleep_length)

def fetch_URLs(query, min_Links_Needed, wd):
    search_URL = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"
    wd.get(search_URL.format(q=query))

    image_URLs = set()
    num_Images = 0
    results_Start = 0
    while num_Images < min_Links_Needed:
        image_URLs = extract_URLs(results_Start, image_URLs)
        if len(image_URLs) >= min_Links_Needed:
            print("FOUND:",len(image_URLs),"image links: proceeding to retrieval...")
            break

        else:
            print("FOUND:",len(image_URLs),"image links: continuing to search...")
            time.sleep(5)
            return
            load_More = wd.find_element_by_css_selector(".mye4qd")
            if load_More:
                wd.execute_script("document.querySelector('.mye4qd').click();")
        results_Start = len(thumbnail_results)
    return image_URLs


def extract_URLs(results_Start, image_URLs):
    scroll_To_End(wd, 1)
    thumbnail_Results = wd.find_elements_by_css_selector("img.Q4LuWd")
    num_Results = len(thumbnail_Results)
    print("FOUND:", num_Results,"search results. Proceeding to extract links number", results_Start, "to", num_Results)
    print(f"Found: {num_Results} search results. Extracting links from {results_Start}:{num_Results}")
    for image in thumbnail_Results[results_Start:num_Results]:
        try:
            image.click()
            time.sleep(1)
        except Exception:
            continue

        found_Images = wd.find_elements_by_css_selector('img.n3VNCb')
        for found_Image in found_Images:
            if found_Image.get_attribute('src') and 'http' in found_Image.get_attribute('src'):
                image_URLs.add(found_Image.get_attribute('src'))
    return(image_URLs)



def download_URLs(folder_Path: str, file_name: str, url: str):
    try:
        image_Contents = requests.get(url).content

    except Exception as e:
        print("ERROR: failed to download",url,e)

    try:
        image_File = io.BytesIO(image_Contents)
        image = Image.open(image_File).convert('RGB')
        folder_Path = os.path.join(folder_Path, file_name)
        if os.path.exists(folder_Path):
            file_Path = os.path.join(folder_Path, hashlib.sha1(image_Contents).hexdigest()[:10] + '.jpg')
        else:
            os.mkdir(folder_Path)
            file_Path = os.path.join(folder_Path, hashlib.sha1(image_Contents).hexdigest()[:10] + '.jpg')
        with open(file_Path, 'wb') as f:
            image.save(f, "JPEG", quality=85)
        print("SUCCESS: saved",url,"as",file_Path)
    except Exception as e:
        print("ERROR: failed to save",url,e)


if __name__ == '__main__':
    wd = webdriver.Chrome(executable_path=driver_Path)
    search_Queries = ["ddlc","monika"]
    for query in search_Queries:
        wd.get('https://google.com')
        search_Box = wd.find_element_by_css_selector('input.gLFyf')
        search_Box.send_keys(query)
        links = fetch_URLs(query, 200, wd)
        images_Path = 'C:/Users/chloe/OneDrive/Desktop/imagescraping'
        for link in links:
            download_URLs(images_Path, query, link)
    print("FINISHED: all queries complete")
    wd.quit()
