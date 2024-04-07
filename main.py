import selenium
from constants import *
from typing import Dict
from processing.image_from_request import PlacesTableRaw, ImageTableRaw
from processing.image_from_request import get_images_by_request, save_pic
import pandas as pd
from pathlib import Path
from enum import Enum
from typing import Callable, TypeAlias
import requests
import tqdm

from dataclasses import *
ParseFunc: TypeAlias = Callable[[Path], pd.DataFrame]

from selenium import webdriver

reference_table_raw = PlacesTableRaw.column_labels()
reference_images_table_raw = ImageTableRaw.column_labels()
print(reference_table_raw)

#func to restructure input dataframe to reference structure.

def get_table(filepath: Path, parse_func: ParseFunc, bind_labels: Dict[str, str]) -> pd.DataFrame:
    raw_table = parse_func(filepath)
    dataframe = pd.DataFrame(columns=list(bind_labels.keys()))
    for ref_label, raw_label in bind_labels.items():
        if raw_label == '':
            continue

        dataframe[ref_label] = raw_table[raw_label]
    
    dataframe.dropna(subset=['Name'], inplace=True)
    dataframe.fillna('')
    return dataframe


def to_table_transform(location, filename, cityname):

    bind_labels={
    #     'xid'        : 'XID',
    #     'name'       : 'Name', 
    #     'category'   : 'Kind',
    #     'city'       : '',
    #     'lat'        : 'Lat', 
    #     'long'       : 'Lon',
    # }
    'XID': 'XID', 
     'Name': 'Name', 
     'Kind':'Kind', 
     'City':'', 
     'OSM':'OSM', 
     'WikiData':'WikiData', 
     'Rate':'Rate',
     'Lon':'Lon', 
     'Lat':'Lat'
     }
    
    data_frame = get_table(filepath=f'{location}/{filename}.xlsx', parse_func=lambda path: pd.read_excel(path), bind_labels=bind_labels)

    data_frame.fillna({'city':f'{cityname}'}, inplace=True)

    data_frame.to_csv(f'{location}/{filename}_new.csv', index=False)



def main():
    to_table_transform(location='./src/csv', filename='NN', cityname="Нижний Новгород")

    # image_dataframe = list()

    # places = pd.read_csv('./src/csv/NN_new.csv')[['name', 'city']]
    # # print(places)
    # i = 0
    # driver = webdriver.Chrome()
    # for _, raw in tqdm.tqdm(places.iterrows(), total=100):
    #     if i < 100:
    #         table_raw = ImageTableRaw(name=raw['name'], city=raw['city'], image='')
    #         images = get_images_by_request(driver, table_raw=table_raw, searching_image_func=None)
    #         for index, image in tqdm.tqdm(enumerate(images)):
    #             im_bytes = requests.get(image).content
    #             # print(im_bytes)
    #             table_raw.write_image_impl(im_bytes)
    #             # print(table_raw)
    #             image_dataframe.append(table_raw.to_csv_raw)
    #             save_pic(url=image, code=index, place_name=f'./src/images/{table_raw.name}/')
    #     i += 1
    # pd.DataFrame(image_dataframe).to_csv('./src/csv/NN_images.csv', index=False)
if __name__ == "__main__":
    main()