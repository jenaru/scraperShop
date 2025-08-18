from abc import ABC, abstractmethod
import httpx
from bs4 import BeautifulSoup

class BaseScraper(ABC):
    def __init__(self, store_name):
        self.store_name = store_name

    @abstractmethod
    def scrape(self, game_name):
        """
        Debe buscar un juego y devolver una lista de diccionarios con:
        {'name': str, 'price': float, 'in_stock': bool, 'url': str}
        """
        pass

    def _get_soup(self, url):
        try:
            response = httpx.get(url, follow_redirects=True, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except httpx.RequestError as e:
            print(f"Error al conectar con {url}: {e}")
            return None