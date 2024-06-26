from typing import Dict, List, TypeAlias
from typing import Callable

import PIL.Image

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from dataclasses import dataclass

import time
import base64
import requests 
import os
import PIL

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



#TODO: replace hardcode column represent to dinamic injection
@dataclass
class PlacesTableRaw:
    """
        Used for dataset raw presentation format)
    """
    xid:         str
    name:        str
    category:    str
    city:        str
    OSM:         str
    wikiData:    str
    rate:        str
    lat:         float
    long:        float
    
    @property
    def to_request(self: "PlacesTableRaw") -> str:
        return " ".join([f'[{str(self.name)}]', f'[{str(self.name)}]'])
    
    @staticmethod
    def column_labels() -> List[str]:
        return ['XID', 'Name', 'Kind', 'City', 'OSM', 'WikiData', 'Rate', 'Lon', 'Lat']
    
@dataclass
class ImageTableRaw:
    """
        Used for dataset raw presentation format)
    """

    name: str
    city: str
    image: bytes
    @staticmethod
    def column_labels() -> List[str]:
        return ['name', 'image', 'city']
    
    
    def write_image_impl(self: 'ImageTableRaw', image: bytes) -> None:
        self.image = str(base64.b64encode(image))[2:-1]
    
    @property
    def to_csv_raw(self) -> Dict[str, bytes]:
        return {
            'name': self.name,
            'image': self.image
        }
    
    @property
    def to_request(self):
        return f'[{self.name}] [{self.city}]'
    
Url: TypeAlias = str
SearchFuction: TypeAlias = Callable[[WebElement], List[WebElement]]

#Эта бяка из плохого файлика) 
#----------------------------------------------------#
# BASE IMPLEMENTATION OF SEARCHING IMAGE BY THE PAGE #
# PLEASE BE MORE ACTRACTIVE WHEN USING THIS FUNC     #
#----------------------------------------------------#
#TODO: seperate the process of searching images from WebElement
def get_images_by_request(driver, table_raw: ImageTableRaw, searching_image_func: SearchFuction=lambda x: x) -> List[Url]:
    
    #TODO: hide driver implementation to syngletone pattern by process
    # driver = webdriver.Chrome()

    #start magick with webdriver
    driver.get('https://yandex.ru/images/search')

    #magick trick. Maybe change delay time to improve performance
    time.sleep(2)

    # fill request on the page 
    request = table_raw.to_request
    print(request)

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


