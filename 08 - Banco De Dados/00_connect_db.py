import sqlite3
from pathlib import Path

ROOT_PATH = Path(__file__).parent # Pegando o caminho da pasta 

connection = sqlite3.connect(ROOT_PATH / 'meu_banco.db') # Criação da database
cur = connection.cursor() # Cria o cursor

# cur.execute('CREATE TABLE IF NOT EXISTS clientes (id INTEGER PRIMARY KEY AUTOINCREMENT, nome VARCHAR(100), email VARCHAR(150))') # Executa o cursor para criação da tabela

# data = [
#   ("Maria", "example@gmail.com"),
#   ("Marcos", "example@gmail.com"),
#   ("Miguel", "example@gmail.com"),
# ]

# data_2 = ("Matheus", "example@gmail.com") 

# cur.executemany("INSERT INTO clientes (nome, email) VALUES (?,?);", data) # o cur.executemany consegue inserir varios dados como uma lista de tuplas por exemplo
# cur.execute("INSERT INTO clientes (nome, email) VALUES (?, ?);", data_2) # o cur.execute, insere apenas um dado por vez


def criar_tabela(cursor):
  cur.execute("CREATE TABLE IF NOT EXISTS clientes (id INTEGER PRIMARY KEY AUTOINCREMENT, nome VARCHAR(100), email VARCHAR(150))"
  )

def inserir_registro(conn, cursor, nome, email):
  data = (nome, email)
  cur.execute("INSERT INTO clientes (nome, email) VALUES (?, ?)", data)
  conn.commit()

def atualizar_registro(conn, cursor, nome, email, id):
  data = (nome, email, id)
  cursor.execute("UPDATE clientes SET nome = ?, email = ? WHERE id = ?", data)
  conn.commit()

def deletar_registro(conn, cursor, id):
  data = (id,)
  cursor.execute("DELETE FROM clientes WHERE id = ?", data)
  conn.commit()

def inserir_lote(conn, cursor, data):
  cursor.executemany("INSERT INTO clientes (nome, email) VALUES (?, ?)", data)
  conn.commit()

# dados = [
#   ("Marcos", "example@gmail.com"),
#   ("Adryann", "example@gmail.com"),
#   ("Maria", "example@gmail.com"),
# ]

# inserir_lote(connection, cur, dados) 

def consultar(cursor, id):
  cursor.execute('SELECT * FROM clientes WHERE id = ?', (id,))
  return cursor.fetchone()

def listar_clientes(conn, cursor):
  cursor.execute("SELECT * FROM clientes")
  return cursor.fetchall()

lista_clientes = listar_clientes(connection, cur)
for cliente in lista_clientes:
  print(cliente)

def recuperar_cliente(cursor, id):
  cursor.row_factory = sqlite3.Row
  cursor.execute("SELECT * FROM clientes WHERE id = ?", (id,))
  result = cursor.fetchone()
  return dict(result)

cliente = recuperar_cliente(cur, 1)
print(f"Bem vindo {cliente["nome"]}, ID: {cliente["id"]}, Email: {cliente["email"]}")