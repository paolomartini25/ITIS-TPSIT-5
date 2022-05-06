from flask import Flask, jsonify, request
import sqlite3
from pathlib import Path
import pandas as pd


dir_path = str(Path(__file__).parent.resolve())

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route("/", methods=["GET"])
def home():
    return "<h1>Biblioteca online</h1><p>Prototipo di web API.</p>"

@app.route("/api/v1/resources/books/all", methods=["GET"])
def api_all():
    con = sqlite3.connect(f'{dir_path}/libri.db')
    libri = pd.read_sql_query("SELECT * FROM libri", con)
    return jsonify(libri.to_dict())

@app.route("/api/v1/resources/books", methods=["GET"])
def api_id():

    con = sqlite3.connect(f'{dir_path}/libri.db')

    if "id" in request.args:
        id = int(request.args["id"])
        libri = pd.read_sql_query(f"SELECT * FROM libri WHERE id = '{id}'", con)

    elif "title" in request.args:
        title = request.args["title"]
        libri = pd.read_sql_query(f"SELECT * FROM libri WHERE title = '{title}'", con)

    else:
        return "Error: No id field provided. Please specify"
    
    
    con.close()
    return jsonify(libri.to_dict())


app.run()