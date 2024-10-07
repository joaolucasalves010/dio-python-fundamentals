import sqlite3
from pathlib import Path

ROOT_PATH = Path(__file__).parent

connection = sqlite3.connect(ROOT_PATH / "meu_banco.db")
cursor = connection.cursor()
cursor.row_factory = sqlite3.Row

id_cliente = input("Informe o ID do  cliente ")
cliente = cursor.execute(f"SELECT * FROM clientes WHERE id = ?", (id_cliente, ))
clientes = cursor.fetchall()

for cliente in clientes:
  print(dict(cliente))