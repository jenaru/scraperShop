from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, joinedload
from typing import List

from . import models, schemas
from .database import SessionLocal, engine
from .scraper.zacatrus import ZacatrusScraper
from .scraper.masqueoca import MasqueocaScraper

# Crea las tablas en la base de datos si no existen
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Board Game Price Comparator API",
    description="API para buscar y comparar precios de juegos de mesa de varias tiendas.",
    version="1.0.0"
)

# --- CORS Middleware ---
# Permite que el frontend (ej. en http://localhost:5173) se comunique con el backend.
origins = [
    "http://localhost",
    "http://localhost:5173", # Puerto por defecto de Vite
    "http://localhost:3000", # Puerto por defecto de Create React App
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"], # Permite todas las cabeceras
)

# --- Dependencia de la Base de Datos ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Endpoints de la API ---

@app.post("/scrape", status_code=201, response_model=schemas.Game)
def run_scraping(scrape_request: schemas.GameCreate, db: Session = Depends(get_db)):
    """
    Ejecuta el scraping para un juego específico, lo guarda en la base de datos
    y devuelve los datos del juego con sus precios.
    Es idempotente: no crea juegos duplicados si ya existen.
    """
    game_name = scrape_request.name
    # Busca si el juego ya existe en la BD (insensible a mayúsculas/minúsculas)
    db_game = db.query(models.Game).filter(models.Game.name.ilike(game_name)).first()

    # Si no existe, lo crea
    if not db_game:
        db_game = models.Game(name=game_name)
        db.add(db_game)
        db.commit()
        db.refresh(db_game)

    # Lista de todos los scrapers a ejecutar
    scrapers = [ZacatrusScraper(), MasqueocaScraper()]

    for scraper in scrapers:
        results = scraper.scrape(game_name)
        for item in results:
            # Busca si ya existe un precio para este juego en esta tienda
            db_price = db.query(models.Price).filter(
                models.Price.game_id == db_game.id,
                models.Price.store == scraper.store_name
            ).first()

            if db_price:
                # Si existe, actualiza el precio y el stock
                db_price.price = item['price']
                db_price.in_stock = item['in_stock']
            else:
                # Si no existe, crea una nueva entrada de precio
                db_price = models.Price(
                    store=scraper.store_name,
                    price=item['price'],
                    in_stock=item['in_stock'],
                    url=item['url'],
                    game_id=db_game.id
                )
                db.add(db_price)

    db.commit()
    db.refresh(db_game)
    return db_game


@app.get("/games", response_model=List[schemas.Game])
def get_all_games(db: Session = Depends(get_db)):
    """
    Devuelve una lista de todos los juegos con sus precios asociados.
    """
    # Usamos joinedload para cargar los precios relacionados en la misma consulta (evita N+1)
    games = db.query(models.Game).options(joinedload(models.Game.prices)).all()
    return games


@app.get("/games/{game_id}", response_model=schemas.Game)
def get_game_details(game_id: int, db: Session = Depends(get_db)):
    """
    Devuelve los detalles de un juego específico por su ID, incluyendo todos sus precios.
    """
    game = db.query(models.Game).options(joinedload(models.Game.prices)).filter(models.Game.id == game_id).first()

    if not game:
        raise HTTPException(status_code=404, detail="Juego no encontrado")
    return game