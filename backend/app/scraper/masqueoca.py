from .base_scraper import BaseScraper
import re

# ¡IMPORTANTE! Estos selectores CSS son un ejemplo y deben ser verificados.
SEARCH_URL = "https://www.masqueoca.com/buscar?controller=search&s={}"
PRODUCT_SELECTOR = ".product-container .product-miniature"
NAME_SELECTOR = ".product-title a"
PRICE_SELECTOR = ".product-price"
# Masqueoca no siempre muestra un indicador de stock claro en la lista,
# a menudo se debe visitar la página del producto. Para este ejemplo,
# asumiremos que si el producto aparece en la búsqueda, está en stock.
STOCK_SELECTOR = ".product-availability" # Esto puede no ser fiable

class MasqueocaScraper(BaseScraper):
    def __init__(self):
        super().__init__("Masqueoca")

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

                # Limpiar el precio: quitar "€", espacios y usar punto como decimal
                price_text = price_element.text.strip()
                price_match = re.search(r'(\d+,\d+)', price_text)
                if not price_match:
                    continue

                price_str = price_match.group(1).replace(',', '.')

                # Comprobar disponibilidad
                stock_element = product.select_one(STOCK_SELECTOR)
                # La lógica de stock puede ser compleja. Un texto como "Añadir al carrito"
                # suele indicar disponibilidad. Aquí simplificamos.
                in_stock = stock_element is not None and "No disponible" not in stock_element.text

                results.append({
                    'name': name,
                    'price': float(price_str),
                    'in_stock': in_stock,
                    'url': name_element['href']
                })
        return results
