from flask import Flask, request, jsonify,send_from_directory
import sqlite3 
import threading
import os

app = Flask(__name__)

#path to the Index.html and DB
base_dir = os.path.dirname(__file__)
frontendPath = os.path.join(base_dir, "..", "frontend")
path = os.path.join(base_dir, "..", "frontend", "index.html")
pathDB = os.path.join(base_dir, "..","..","DataBase","TimeStorage.db")

with open(path, "r", encoding="utf-8") as f:
    html_content = f.read()

def Dbconn(mes):
    conn = sqlite3.connect(pathDB)
    cur = conn.cursor()
    cur.execute("SELECT day, time FROM time WHERE month = ? ORDER BY day", (mes,))
    dados = cur.fetchall()
    conn.close()
    return [{"dia": day, "tempo": time} for day, time in dados]

@app.route("/")
def hello_world():
    return  html_content

@app.route("/script.js")
def serve_script():
    return send_from_directory(frontendPath, "script.js")

@app.route("/style.css")
def serve_style():
    return send_from_directory(frontendPath, "style.css")

@app.route("/dados")
def dados():
    mes = request.args.get("mes", 1, type=int)
    dados = Dbconn(mes)
    return jsonify(dados)

def RunServer():
    app.run(debug=False, port=5000)

RunServer()