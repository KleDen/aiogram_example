class Item:
    id = 0

    def __init__(self, photo_url: str):
        Item.id += 1
        self.id = Item.id
        self.photo_url = photo_url


course = Item('https://kurs.com.ua/storage/images/icons/260.png')
carrot = Item('https://i5.walmartimages.ca/images/Enlarge/686/686/6000198686686.jpg')
