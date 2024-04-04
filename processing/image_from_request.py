from typing import List, TypeAlias
from typing import Callable
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from dataclasses import dataclass
import time

import requests 
import os

from constants import *

# SOME IMPLEMENTATION OF SAVING IMAGE FROM URL
def save_pic(url: str, code: int, place_name: str) -> None:
    try:
        file_path = f'{place_name}/{code}.jpg'

        if not os.path.exists(place_name):
            os.mkdir(place_name)

        if not os.path.exists(file_path):
            image = requests.get(url)
            with open(file_path, 'wb') as image_file:
                image_file.write(image.content)
                image_file.close()      
    except:
        print(f"{url} - image file failed to be written")


@dataclass
class TableRaw:
    """
        Representation of table columns structure of the dataset. \n
        Used for dataset raw presentation format)
    """
    category: str
    name:     str
    long:     float
    lat:      float
    img:      str

    @property
    def to_request(self: "TableRaw") -> str:
        return " ".join([self.name, self.img, str(self.lat), str(self.long)])
    
    @property
    def column_labels(self: "TableRaw") -> List[str]:
        return ['name', 'lat', 'long', 'category', 'img']
    

SearchFuction: TypeAlias = Callable[[WebElement], List[WebElement]]
Url: TypeAlias = str

#Эта бяка и плохого файлика) 
#----------------------------------------------------#
# BASE IMPLEMENTATION OF SEARCHING IMAGE BY THE PAGE #
# PLEASE BE MORE ACTRACTIVE WHEN USING THIS FUNC          #
#----------------------------------------------------#
#TODO: seperate the process of searching images from WebElement
def get_images_by_request(table_raw: TableRaw, searching_image_func: SearchFuction=lambda x: x) -> List[Url]:

    #TODO: hide driver implementation to syngletone pattern
    driver = webdriver.Chrome()

    #start magick with webdriver
    driver.get('https://yandex.ru/images/search')

    #magick trick. Maybe change delay time to improve performance
    time.sleep(1)

    # fill request on the page
    request  = table_raw.to_request

    input_el = driver.find_element(By.TAG_NAME, 'input')
    input_el.send_keys(request)

    # find submit button to sent request
    btn = driver.find_element(By.CSS_SELECTOR, '*[type="submit"]')
    driver.execute_script("arguments[0].click();", btn)

    # magick trick too...
    time.sleep(2)

    # PLEASE CHANGE THIS
    # find images from the page
    div = driver.find_element(By.CLASS_NAME, 'SerpList-Content')
    # elements = div.find_elements(By.CLASS_NAME, 'SimpleImage-Image_clickable')
    elements = div.find_elements(By.TAG_NAME, 'img')

    images = [el.get_attribute('src') for el in elements]
    return images


