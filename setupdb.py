"""Recria o banco de dados de desenvolvimento a partir de database.sql."""

from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent

# Abre (ou cria) o arquivo do SQLite e executa todo o script de modelagem.
with sqlite3.connect(BASE_DIR / "database.db") as connection:
    with open(BASE_DIR / "database.sql", "r", encoding="utf-8") as file:
        connection.executescript(file.read())

print("Banco de dados preparado com sucesso!")
