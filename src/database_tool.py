import sqlite3
from pathlib import Path


def run_sql_query(query):

    database_path = Path("database/delivery.db")

    # Verifica se a consulta começa com SELECT ou WITH
    normalized_query = query.strip()

    if not normalized_query.upper().startswith(("SELECT", "WITH")):
        return {"erro": "Apenas consultas SELECT e WITH são permitidas."}

    # Abre o banco em modo somente leitura
    connection = sqlite3.connect(
        f"file:{database_path.resolve()}?mode=ro",
        uri=True
    )

    connection.row_factory = sqlite3.Row

    # Define quais operações o SQLite pode executar
    allowed_actions = {
        sqlite3.SQLITE_SELECT,
        sqlite3.SQLITE_READ,
        sqlite3.SQLITE_FUNCTION
    }

    if hasattr(sqlite3, "SQLITE_RECURSIVE"):
        allowed_actions.add(sqlite3.SQLITE_RECURSIVE)

    def authorize(action, arg1, arg2, database, trigger):
        if action in allowed_actions:
            return sqlite3.SQLITE_OK

        return sqlite3.SQLITE_DENY

    try:
        # Ativa a proteção antes de executar a consulta
        connection.set_authorizer(authorize)

        cursor = connection.cursor()

        # Limita o retorno a 100 registros
        limited_query = (
            f"SELECT * FROM ({normalized_query.rstrip(';')}) "
            "AS limited_result LIMIT 100"
        )

        cursor.execute(limited_query)

        results = cursor.fetchall()

        return [dict(row) for row in results]

    except sqlite3.Error as error:
        return {"erro": str(error)}

    finally:
        connection.close()