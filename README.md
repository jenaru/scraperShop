# Comparador de Precios de Juegos de Mesa

Este proyecto es una aplicación web full-stack que permite a los usuarios buscar juegos de mesa y comparar sus precios en varias tiendas online. La aplicación obtiene los datos en tiempo real mediante un sistema de web scraping modular y los presenta en una interfaz limpia y moderna.

## Stack Tecnológico

La aplicación está construida con las siguientes tecnologías:

-   **Backend:**
    -   **Python 3.9+**
    -   **FastAPI:** Para construir una API web moderna y de alto rendimiento.
    -   **SQLAlchemy:** Como ORM para la interacción con la base de datos.
    -   **PostgreSQL:** Como base de datos relacional.
    -   **BeautifulSoup4 & httpx:** Para las tareas de web scraping.
-   **Frontend:**
    -   **React 18+** (con Vite)
    -   **React Router DOM:** Para la navegación y el enrutamiento del lado del cliente.
    -   **TailwindCSS:** Para un diseño de UI moderno y personalizable.
    -   **shadcn/ui:** Una colección de componentes de UI reutilizables.
    -   **axios:** Para realizar las peticiones a la API del backend.
-   **Orquestación:**
    -   **Docker & Docker Compose:** Para contenerizar la aplicación y gestionar el entorno de desarrollo y producción de forma consistente.

## Cómo Levantar el Entorno

Gracias a Docker, levantar todo el entorno de desarrollo es muy sencillo. Solo necesitas tener **Docker** y **Docker Compose** instalados en tu máquina.

Sigue estos pasos:

1.  **Clona el repositorio:**
    ```bash
    git clone <URL-del-repositorio>
    cd <nombre-del-directorio>
    ```

2.  **Levanta los servicios con Docker Compose:**
    Desde la raíz del proyecto, ejecuta el siguiente comando. La primera vez, Docker descargará las imágenes base y construirá los contenedores, lo que puede tardar unos minutos.

    ```bash
    docker-compose up --build
    ```

    Este comando hará lo siguiente:
    -   Construirá las imágenes de Docker para el `frontend` y el `backend`.
    -   Iniciará los tres contenedores: `db` (PostgreSQL), `backend` y `frontend`.
    -   Creará una red interna para que los contenedores se comuniquen entre sí.

3.  **Accede a la aplicación:**
    -   El **frontend** estará disponible en `http://localhost:5173`.
    -   La **API del backend** estará accesible en `http://localhost:8000`.
    -   La **documentación interactiva de la API** (generada por FastAPI) se encontrará en `http://localhost:8000/docs`.

## Cómo Añadir un Nuevo Scraper

El sistema está diseñado para ser fácilmente extensible con nuevos scrapers para otras tiendas. Para añadir una nueva tienda, sigue estos pasos:

1.  **Crea un nuevo archivo de Scraper:**
    En el directorio `backend/app/scraper/`, crea un nuevo archivo Python (ej: `nombre_tienda.py`).

2.  **Implementa la clase del Scraper:**
    Dentro del nuevo archivo, crea una clase que herede de `BaseScraper` (que se encuentra en `base_scraper.py`). Debes implementar el método `scrape(self, game_name)`.

    ```python
    from .base_scraper import BaseScraper

    class NuevaTiendaScraper(BaseScraper):
        def __init__(self):
            # Llama al constructor de la clase base con el nombre de la tienda
            super().__init__("Nombre de la Tienda")

        def scrape(self, game_name):
            # 1. Construye la URL de búsqueda de la tienda
            search_url = f"https://tienda.ejemplo.com/buscar?q={game_name}"

            # 2. Obtén el 'soup' de la página usando el método heredado
            soup = self._get_soup(search_url)
            if not soup:
                return []

            results = []
            # 3. Usa los selectores CSS para encontrar los productos
            products = soup.select(".selector-del-producto")

            for product in products:
                # 4. Extrae nombre, precio, stock y URL de cada producto
                name = product.select_one(".selector-del-nombre").text.strip()
                price_str = product.select_one(".selector-del-precio").text
                # ... (limpia el precio para convertirlo a float)

                # 5. Añade el resultado a la lista
                results.append({
                    'name': name,
                    'price': float(price_str),
                    'in_stock': True, # o la lógica que determine el stock
                    'url': product.select_one("a")['href']
                })

            return results
    ```

3.  **Registra el nuevo Scraper en la API:**
    Abre `backend/app/main.py` y añade tu nuevo scraper a la lista de scrapers en el endpoint `POST /scrape`.

    ```python
    # En backend/app/main.py
    from .scraper.nombre_tienda import NuevaTiendaScraper # ¡Importa tu nueva clase!

    @app.post("/scrape", ...)
    def run_scraping(...):
        # ...
        # Añade una instancia de tu nuevo scraper a esta lista
        scrapers = [ZacatrusScraper(), MasqueocaScraper(), NuevaTiendaScraper()]
        # ...
    ```

4.  **Reconstruye los contenedores:**
    Para que los cambios surtan efecto, debes reconstruir la imagen del backend.

    ```bash
    docker-compose up --build
    ```

¡Y eso es todo! La próxima vez que se llame al endpoint de scraping, tu nuevo scraper se ejecutará junto con los demás.
