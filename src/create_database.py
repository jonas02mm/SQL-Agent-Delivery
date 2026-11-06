import sqlite3
from pathlib import Path

# Define os caminhos dos arquivos
database_path = Path("database/delivery.db")
schema_path = Path("database/schema.sql")

# Verifica se o banco já existe
if database_path.exists():
    print("O banco de dados já existe.")
else:
    # Conecta ao banco SQLite
    connection = sqlite3.connect(database_path)

    # Ativa a validação dos relacionamentos entre tabelas
    connection.execute("PRAGMA foreign_keys = ON")

    # Lê o arquivo SQL
    schema = schema_path.read_text(encoding="utf-8")

    # Executa os comandos de criação das tabelas
    connection.executescript(schema)

    # Encerra a conexão
    connection.close()

    print("Banco de dados criado com sucesso!")