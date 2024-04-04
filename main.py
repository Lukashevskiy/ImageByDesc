import selenium
from constants import *
from processing.image_from_request import TableRaw
from processing.image_from_request import get_images_by_request
def main():
    print(get_images_by_request(description=TableRaw("Памятник Ленину", "Монументы", 0, 0, ""), searching_image_func=None))
    


if __name__ == "__main__":
    main()