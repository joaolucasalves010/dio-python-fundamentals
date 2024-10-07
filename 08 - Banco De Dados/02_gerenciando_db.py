import sqlite3
from pathlib import Path

ROOT_PATH = Path(__file__).parent

connection = sqlite3.connect(ROOT_PATH / "meu_banco.db")
cursor = connection.cursor()
cursor.row_factory = sqlite3.Row

try:
  cursor.execute("INSERT INTO clientes (nome, email) VALUES (?,?)", ('Teste2', 'teste2@gmail.com'))
  cursor.execute("INSERT INTO clientes (id, nome, email) VALUES (?,?,?)", (2, 'Teste3', 'teste3@gmail.com'))
  connection.commit()
except Exception as exc:
  print(f"Um erro ocorreu {exc}")
  connection.rollback()
