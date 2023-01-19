from bs4 import BeautifulSoup
import requests
import zipfile
import glob
import os

# this is for multi-threading
from concurrent.futures import ThreadPoolExecutor, as_completed

page_no = [i for i in range(1, 5)]

for no in page_no:
    url = "https://www.manaboza17.com/comic/ep_list/16/" + str(no)
    image_url = "https://www.manaboza17.com/comic/ep_view/16/"
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")


    # get "data-episode-id" from "a" tag
    temp_list = soup.find_all("a", attrs={"class":"flex-container episode-items"})

    # get "episode_stitle" from "p" tag
    title_list = soup.find_all("p", attrs={"class":"episode_stitle"})


    # for title, code in zip(title_list, temp_list):
    #     print(title.get_text(), code["data-episode-id"])
    #     soup = BeautifulSoup(requests.get(image_url + code["data-episode-id"]).text, "lxml")

    #     img_list = soup.find_all("div", attrs={"class":"comic_content"})

    #     for image in img_list:
    #         # find all "data-src" from img
    #         candidates = image.find_all("img")
    #         for candidate in candidates:
    #             print(candidate["data-src"])
    #             print(candidate["title"])
                
    #             # save image url = candidate["data-src"], title = candidate["title"]
    #             with open(candidate["title"] + ".jpg", "wb") as f:
    #                 image = requests.get("https:" + candidate["data-src"])
    #                 f.write(image.content)
        
    #     jpg_files = glob.glob("*.jpg")
    #     # zip .jpg files
    #     with zipfile.ZipFile(title.get_text() + ".zip", "w") as myzip:
    #         for jpg_file in jpg_files:
    #             myzip.write(jpg_file)
    #             # delete .jpg files
    #             os.remove(jpg_file)

        
                
    def save_image(url, title):
        with open(title + ".jpg", "wb") as f:
            image = requests.get(url)
            f.write(image.content)


    # this code below is for multi-threading
    with ThreadPoolExecutor() as executor:
        futures = []
        for title, code in zip(title_list, temp_list):
            print(title.get_text(), code["data-episode-id"])
            soup = BeautifulSoup(requests.get(image_url + code["data-episode-id"]).text, "lxml")

            img_list = soup.find_all("div", attrs={"class":"comic_content"})

            for image in img_list:
                # find all "data-src" from img
                candidates = image.find_all("img")
                for candidate in candidates:
                    # print(candidate["data-src"])
                    # print(candidate["title"])
                    future = executor.submit(save_image, "https:" + candidate["data-src"], candidate["title"])
                    futures.append(future)

            for future in as_completed(futures):
                future.result()
            jpg_files = glob.glob("*.jpg") 
            
            with zipfile.ZipFile(candidate["title"] + ".zip", "w") as myzip:
                for jpg_file in jpg_files:
                    myzip.write(jpg_file)
                    # delete .jpg files
                    os.remove(jpg_file)
    