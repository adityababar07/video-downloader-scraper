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

seen = []

with open("seen.txt", "r")  as f:
    seen.extend(iter(f))
    f.close()

def film():
    # choice = categories[random.randint(0, len(categories))-1].replace(" ", "-")
    # # If you want to remove the new lines ('\n'), you can use strip().
    # choice = str(choice).strip()

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

    videos = bs.find_all('div', class_="6u")

    video = videos[random.randint(0, len(videos)-1)].find_all("a", class_="image featured non-overlay atfib n8hu6s")

    video_link = video[0].get('href')
    
    if video_link not in seen:

        video_preview = video[0].find_all('div', class_="hide_noscript")

        extractor = URLExtract()
        count=0
        for img in video_preview:
           image = img.get('onmouseover')
           image = extractor.find_urls(image)
           count+=1
           os.system(f"wget https://{image[0]} -O preview_images/{count}.jpg")
#   
#        count=0
#        for _ in range(10):
#            count+=1
#            image = Image.open(f"preview_images/{count}.jpg")  
#            image.show()
#            time.sleep(5)
#            os.system(f"rm preview_images/{count}.jpg")
        return video_link
    else:
        exit
while True:
    video_link = film()
    # video_link

    time.sleep(5)
    print(f"https://example.com{video_link}")
    with open("seen.txt", 'a') as f:
        '''
        How do you append to a file in Python

with open("test.txt", "a") as myfile:
    myfile.write("appended text")
        '''
        f.write(f"{video_link} \n")
        f.close()
    
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

        time.sleep(10)
        bs = BeautifulSoup(ff_driver.page_source, 'html.parser') 

        # with open("main.html", 'w+') as f:
        #     f.write(str(bs))
        #     f.close()

        frame = bs.find_all("div", id="playerWrapper")

        frame = frame[0].find_all("iframe")
        frame = frame[0].get('src')

        ff_driver.get(f"https:{frame}")
        time.sleep(10)
        bs = BeautifulSoup(ff_driver.page_source, 'html.parser') 
        # with open("main.html", 'w+') as f:
        #     f.write(str(bs))
        #     f.close()
        procede = "n"
        while procede != "y":
            quality = int(input("enter the quality(360/720/1080):\t"))
            if quality == 360:
                video = bs.find_all("source", title="360p")
                if len(video) == 0:
                    video = bs.find_all("source", title="360p60")
        
            elif quality == 720:
                video = bs.find_all("source", title="720p")
                if len(video) == 0:
                    video = bs.find_all("source", title="720p60")
                    if len(video) == 0:
                        video = bs.find_all("source", title="720p HD")
        
            elif quality == 1080:
                video = bs.find_all("source", title="1080p")
                if len(video) == 0:
                    video = bs.find_all("source", title="1080p60")              
                    if len(video) == 0:
                        video = bs.find_all("source", title="1080p Full HD")
            
            video_size = os.system(f"video_size=$(curl --head https:{video[0].get('src')})")
            video_size = os.system("echo $video_size  | awk '/Content-Length/ {print $16}'")
            print(video_size)
            procede=input("do you want to procede (y/n):\t")
        video = video[0].get("src")
        ff_driver.close()
        with open("video_id", "r") as f:
            filename0 = f.read()
            f.close()
        filename = int(filename0) + 1

        with open("video_id", "w") as f:
            f.write(str(filename))
            f.close()
        os.system(f"wget https:{video} -O videos/{filename0}.mp4")
        time.sleep(10)
        print(f" it took {time_1/60000} mins")
        exit()

    else:
        continue
