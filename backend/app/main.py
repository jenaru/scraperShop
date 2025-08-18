from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from .database import SessionLocal, engine
from .scraper.zacatrus import ZacatrusScraper # Importar los scrapers que crees
# ... y otros

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependencia para obtener la sesión de la BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/games", response_model=list[schemas.Game])
def get_all_games(db: Session = Depends(get_db)):
    games = db.query(models.Game).all()
    return games

@app.get("/games/{name}", response_model=schemas.Game)
def get_game_details(name: str, db: Session = Depends(get_db)):
    game = db.query(models.Game).filter(models.Game.name.ilike(f"%{name}%")).first()
    if not game:
        raise HTTPException(status_code=404, detail="Juego no encontrado")
    return game

@app.post("/scrape")
def run_scraping(game_name: str, db: Session = Depends(get_db)):
    # Lista de todos tus scrapers
    scrapers = [ZacatrusScraper()] # Añade aquí instancias de cada scraper

    for scraper in scrapers:
        results = scraper.scrape(game_name)
        for item in results:
            # Lógica para guardar en la BD:
            # 1. Buscar si el juego ya existe. Si no, crearlo.
            # 2. Añadir o actualizar el precio para esa tienda.
            # ... (esta lógica requiere cuidado para evitar duplicados)
            pass 
    return {"status": "Scraping completado", "game": game_name}