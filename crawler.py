from typing import List
from constants import OtoDomConfig, Page
import requests
from bs4 import BeautifulSoup as bs
from abc import ABC, abstractmethod

class Flat:
    def __init__(self, title, link):
        self.title = title
        self.link = link

    def fill_flat(self, description, metrage, price, rooms, floor, additional_costs):
        self.description = description
        self.price = price
        self.metrage = metrage
        self.rooms = rooms
        self.floor = floor
        self.additional_costs = additional_costs

    def print(self):
        return f'''
        *{self.title}*
        {self.link}
        *Price:* {self.price}
        *Rooms:* {self.rooms}
        *Floor:* {self.floor}
        *Metrage:* {self.metrage}
        *Rent costs:* {self.additional_costs}
        =====================================
        *Description:" {self.description}
        '''

    def __repr__(self) -> str:
        return f"Flat: {self.link}"

class Crawler(ABC):
    
    @abstractmethod
    def get_offers(self):
        """Get all offers; Fill jobs list"""
        pass

    @abstractmethod
    def get_offer_detail(self):
        """Fill detail about job"""
        pass

    @abstractmethod
    def fill_offers(self):
        """Fill all offer with get_offer_detail method"""
        pass


class OtoDom(Crawler):

    def __init__(self, conf: Page = OtoDomConfig):
        self.conf = conf
        self.flats = self.get_offers()
        self.fill_offers()

    def extract_metadata(self, content, label):
        try:
            metadata = content.findAll("div", {"aria-label": label})[0].find_all('div')[-1].get_text()
        except IndexError:
            metadata = ''
        return metadata
    
    def get_offers(self) -> List[Flat]:
        website_request = requests.get(self.conf.search_link, timeout=10)
        website_content = bs(website_request.content, 'html.parser')
        return [Flat(title=item.get_text(), link=f"{self.conf.base_link}{item.attrs['href']}") for item in website_content.find_all() if 'data-cy' in item.attrs and 'listing-item-link' == item['data-cy']]

    def get_offer_detail(self, flat: Flat):
        details_page = requests.get(flat.link, timeout=5)
        content = bs(details_page.content, 'html.parser')
        additional_costs = self.extract_metadata(content, 'Czynsz - dodatkowo')
        metrage = self.extract_metadata(content, 'Powierzchnia')
        rooms = self.extract_metadata(content, 'Liczba pokoi')
        floor = self.extract_metadata(content, 'Piętro')
        price = content.find("strong", {"aria-label": "Cena"}).get_text()
        description = content.find("div", {"data-cy": "adPageAdDescription"}).get_text().strip()

        flat.fill_flat(
            description=description,
            metrage=metrage,
            price=price,
            rooms=rooms,
            floor=floor,
            additional_costs=additional_costs
        )

    def fill_offers(self):
        for flat in self.flats:
            self.get_offer_detail(flat)

    def __getitem__(self, index):
        return self.flats[index]

    def __len__(self):
        return len(self.flats)

    def __iter__(self):
        return (f for f in self.flats)

    

if __name__ == "__main__":
    crawler = OtoDom()

    for flat in crawler:
        print(flat.print())