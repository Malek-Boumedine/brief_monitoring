"""Configuration de la base de données et gestion des sessions.

Ce module gère la connexion à la base de données
et fournit une fonction générateur pour obtenir des sessions de base de données.
"""

import os
from sqlmodel import Session, create_engine

# Utiliser SQLite par défaut si DATABASE_URL n'est pas défini
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "sqlite:///./items.db"  # Base SQLite locale
)

POOL_SIZE = 10

# Pour SQLite, on n'utilise pas de pool
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)


def get_db():
    with Session(engine) as session:
        yield session
