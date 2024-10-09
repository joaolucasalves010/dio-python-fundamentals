from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
  nome = "João Lucas"
  return f"<h1>Hello {nome}!</h1>"