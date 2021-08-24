from dataclasses import dataclass


@dataclass 
class Page:
    base_link: str
    search_link: str

OtoDomConfig = Page(
    search_link='https://www.otodom.pl/pl/oferty/wynajem/mieszkanie/wiele-lokalizacji?areaMin=40&distanceRadius=0&market=ALL&page=1&limit=72&by=DEFAULT&direction=DESC&locations%5B0%5D%5BregionId%5D=11&locations%5B0%5D%5BcityId%5D=40&locations%5B0%5D%5BdistrictId%5D=140&locations%5B0%5D%5BsubregionId%5D=439&locations%5B1%5D%5BregionId%5D=11&locations%5B1%5D%5BcityId%5D=40&locations%5B1%5D%5BdistrictId%5D=16&locations%5B1%5D%5BsubregionId%5D=439&locations%5B2%5D%5BregionId%5D=11&locations%5B2%5D%5BcityId%5D=40&locations%5B2%5D%5BdistrictId%5D=1688&locations%5B2%5D%5BsubregionId%5D=439&locations%5B3%5D%5BregionId%5D=11&locations%5B3%5D%5BcityId%5D=40&locations%5B3%5D%5BdistrictId%5D=136&locations%5B3%5D%5BsubregionId%5D=439',
    base_link='https://www.otodom.pl'
    )