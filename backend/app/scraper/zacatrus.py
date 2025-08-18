from .base_scraper import BaseScraper

# ¡IMPORTANTE! Estos selectores CSS son un ejemplo.
# Deberás inspeccionar cada web para obtener los correctos, y pueden cambiar con el tiempo.
SEARCH_URL = "https://zacatrus.es/catalogsearch/result/?q={}"
PRODUCT_SELECTOR = ".product-item-info"
NAME_SELECTOR = ".product-item-name a"
PRICE_SELECTOR = ".price"
STOCK_SELECTOR = ".stock.available" # O la clase que indique que hay stock

class ZacatrusScraper(BaseScraper):
    def __init__(self):
        super().__init__("Zacatrus")

    def scrape(self, game_name):
        search_query = game_name.replace(" ", "+")
        soup = self._get_soup(SEARCH_URL.format(search_query))
        if not soup:
            return []

        results = []
        products = soup.select(PRODUCT_SELECTOR)

        for product in products:
            name_element = product.select_one(NAME_SELECTOR)
            price_element = product.select_one(PRICE_SELECTOR)
            
            if name_element and price_element:
                name = name_element.text.strip()
                # Limpiar el precio (quitar €, comas, etc.)
                price_str = price_element.text.strip().replace('€', '').replace(',', '.').strip()
                
                results.append({
                    'name': name,
                    'price': float(price_str),
                    'in_stock': bool(product.select_one(STOCK_SELECTOR)),
                    'url': name_element['href']
                })
        return results