import requests
import time
import ssl
import re
from PIL import Image
import os
import random
from urlextract import URLExtract
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


time_1 = time.perf_counter()

categories = []

with open("categories.txt", "r")  as f:
    
    '''
    Sourcery - Replace a for append loop with list extend, Simplify generator expressionsourcery(refactoring:for-append-to-extend;simplify-generator)
for categorie in f: categories.append(categorie)
Full name: main1.categorie

Lines 15-16 refactored with the following changes:

Replace a for append loop with list extend (for-append-to-extend)
Simplify generator expression (simplify-generator)
 categories = []
 
 with open("categories.txt", "r")  as f:
-    for categorie in f:
-        categories.append(categorie)
+    categories.extend(iter(f))'''
    categories.extend(iter(f))
    f.close()

def film():
    choice = categories[random.randint(0, len(categories))-1].replace(" ", "-")
    # If you want to remove the new lines ('\n'), you can use strip().
    choice = str(choice).strip()

    # html = requests.get(f"https://example.com/category/{choice}".replace(" ", "+"))
    html = requests.get("https://example.com/")
    bs = BeautifulSoup(html.text, 'html.parser') 
    ''''r'       open for reading (default)
    'w'       open for writing, truncating the file first
    'x'       create a new file and open it for writing
    'a'       open for writing, appending to the end of the file if it exists
    'b'       binary mode
    't'       text mode (default)
    '+'       open a disk file for updating (reading and writing)
    'U'       universal newline mode (deprecated)'''
    with open("main.html", 'w+') as f:
        f.write(str(bs))
        f.close()

    no_of_videos = bs.find_all('div', class_="box page-content")

    no_of_videos = no_of_videos[1].find_all('p')

    no_of_videos = int(no_of_videos[0].text.replace(" high definition videos are available for you",""))

    if no_of_videos%46==0:
        no_of_pages = no_of_videos//46
    else:
        no_of_pages = (no_of_videos//46)+1

    page = random.randint(1, no_of_pages)

    html = requests.get(f"https://example.com/category/{choice}/{random.randint(1, no_of_pages)}".replace(" ", "+"))
    bs = BeautifulSoup(html.text, 'html.parser') 

    with open("main.html", 'w+') as f:
        f.write(str(bs))
        f.close()

    videos = bs.find_all('div', class_="6u")

    video = videos[random.randint(0, len(videos)-1)].find_all("a", class_="image featured non-overlay atfib")

    video_link = video[0].get('href')

    video_preview = video[0].find_all('div', class_="hide_noscript")

    extractor = URLExtract()
#    count=0
#    for img in video_preview:
#        image = img.get('onmouseover')
#        image = extractor.find_urls(image)
#        count+=1
#        os.system(f"wget https://{image[0]} -O preview_images/{count}.jpg")
#
#    count=0
#    for _ in range(10):
#        count+=1
#        image = Image.open(f"preview_images/{count}.jpg")  
#        image.show()
#        time.sleep(5)
#        os.system(f"rm preview_images/{count}.jpg")
    return video_link
while True:
    video_link = film()
    video_link
    time.sleep(5)
    choice = input("\n \n Do you want to download the video?(y/n) :- ")

    if choice == "y":
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        firefox_profile = Options()
        firefox_profile.add_argument("--headless")
        # firefox_profile.add_argument("--window - size = 1920, 1080")
        firefox_profile.set_preference("browser.privatebrowsing.autostart", True)
        ff_driver = webdriver.Firefox(options=firefox_profile)
        # ff_driver.minimize_window()

        ff_driver.get(f"https://example.com{video_link}")
        print(f"https://example.com{video_link}")
        time.sleep(10)
        bs = BeautifulSoup(ff_driver.page_source, 'html.parser') 

        with open("main.html", 'w+') as f:
            f.write(str(bs))
            f.close()

        frame = bs.find_all("div", id="playerWrapper")

        frame = frame[0].find_all("iframe")
        frame = frame[0].get('src')

        ff_driver.get(f"https:{frame}")
        time.sleep(10)
        bs = BeautifulSoup(ff_driver.page_source, 'html.parser') 
        with open("main.html", 'w+') as f:
            f.write(str(bs))
            f.close()

        video = bs.find_all("source", title="1080p")
        if len(video) == 0:
            video = bs.find_all("source", title="720p")
            if len(video) == 0:
                video = bs.find_all("source", title="320p")
                if len(video) == 0:
                    video = bs.find_all("source", title="320p60")
                    if len(video) == 0:
                        video = bs.find_all("source", title="720p60")
                        if len(video) == 0:
                            video = bs.find_all("source", title="1080p60")
                            if len(video) == 0:
                                video = bs.find_all("source", title="720p HD")
                                if len(video) == 0:
                                    video = bs.find_all("source", title="1080p Full HD")
        video = video[0].get("src")
        ff_driver.close()
        os.system(f"wget https:{video}")
        time.sleep(10)
        print(f" it took {time_1/60000} mins")
        exit()

    else:
        continue
