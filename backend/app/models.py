from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql://user:password@db:5432/boardgames"
# O para SQLite:
# DATABASE_URL = "sqlite:///./boardgames.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Game(Base):
    __tablename__ = "games"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    prices = relationship("Price", back_populates="game")

class Price(Base):
    __tablename__ = "prices"
    id = Column(Integer, primary_key=True, index=True)
    store = Column(String, index=True)
    price = Column(Float)
    in_stock = Column(Boolean, default=True)
    url = Column(String)
    game_id = Column(Integer, ForeignKey("games.id"))
    game = relationship("Game", back_populates="prices")

# Crea las tablas si no existen
Base.metadata.create_all(bind=engine)