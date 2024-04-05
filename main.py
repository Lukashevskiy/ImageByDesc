import selenium
from constants import *
from typing import Dict
from processing.image_from_request import TableRaw
from processing.image_from_request import get_images_by_request, save_pic
import pandas as pd
from pathlib import Path
from enum import Enum
from typing import Callable, TypeAlias

from dataclasses import *
ParseFunc: TypeAlias = Callable[[Path], pd.DataFrame]


reference_table_raw = TableRaw.column_labels()
print(reference_table_raw)

#func to restructure input dataframe to reference structure.

def get_table(filepath: Path, parse_func: ParseFunc, bind_labels: Dict[str, str]) -> pd.DataFrame:
    raw_table = parse_func(filepath)
    dataframe = pd.DataFrame(columns=list(bind_labels.keys()))
    for ref_label, raw_label in bind_labels.items():
        if raw_label == '':
            continue

        dataframe[ref_label] = raw_table[raw_label]
    
    dataframe.dropna(subset=['name'], inplace=True)
    dataframe.fillna('')
    return dataframe

def main():
    # print(pd.read_excel('./src/csv/sample.xlsx')['Name'].isna().sum())

    bind_labels={
        'name'       : 'Name', 
        'category'   : 'Kind', 
        'lat'        : 'Lat', 
        'long'       : 'Lon',
        'img'        : '',
        'description': ''
    }
    
    data_frame = get_table(filepath='./src/csv/sample.xlsx', parse_func=lambda path: pd.read_excel(path), bind_labels=bind_labels)
    # print(data_frame)
    data_frame.to_csv('./src/csv/sample_new.csv', index=False)

    for _, raw in data_frame.iterrows():
        print(raw)
        table_raw = TableRaw(*raw)
        images = get_images_by_request(table_raw=table_raw, searching_image_func=None)
        for index, image in enumerate(images):
            table_raw.img = image
            data_frame.add(asdict(table_raw))
            save_pic(url=image, code=index, place_name=f'./src/images/{table_raw.name}/')
    


if __name__ == "__main__":
    main()