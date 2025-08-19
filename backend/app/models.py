from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# La URL de la base de datos se leerá desde las variables de entorno en un entorno real,
# pero para Docker Compose, la URL se puede definir aquí o pasarla al crear el engine.
DATABASE_URL = "postgresql://user:password@db:5432/boardgames"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    prices = relationship("Price", back_populates="game", cascade="all, delete-orphan")

class Price(Base):
    __tablename__ = "prices"

    id = Column(Integer, primary_key=True, index=True)
    store = Column(String, index=True, nullable=False)
    price = Column(Float, nullable=False)
    in_stock = Column(Boolean, default=True)
    url = Column(String, nullable=False)

    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    game = relationship("Game", back_populates="prices")

# Esta línea es opcional si usas Alembic para migraciones, pero útil para un inicio rápido.
# En main.py ya se llama, así que aquí podría ser redundante, pero no hace daño.
# Base.metadata.create_all(bind=engine)