from flask import Flask, request, jsonify
import json, os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

INVENTARIO_FILE = "inventarios_recibidos.json"
JSON_AGENCIA = "inventario_render.json"
NOMBRE_AGENCIA = "matriz"

def cargar_inventario():
    if not os.path.exists(INVENTARIO_FILE):
        return []
    try:
        with open(INVENTARIO_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def guardar_inventario(data):
    with open(INVENTARIO_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.route("/")
def home():
    return f"Servidor PROXI JQ Motors {NOMBRE_AGENCIA} activo."

@app.route("/inventario", methods=["POST"])
def recibir_inventario():
    data = request.get_json() or {}
    agencia = data.get("agencia", NOMBRE_AGENCIA)
    inventario = data.get("inventario", [])

    inventario_final = [
        {
            "codigo": i.get("codigo", ""),
            "descripcion": i.get("descripcion", ""),
            "stock": i.get("stock", 0),
            "agencia": agencia
        } for i in inventario
    ]

    guardar_inventario(inventario_final)
    return jsonify({"status": "actualizado"})

@app.route("/inventario-json", methods=["GET"])
def obtener_inventario():
    return jsonify(cargar_inventario())

@app.route("/limpiar", methods=["POST"])
def limpiar_inventario():
    guardar_inventario([])
    return jsonify({"statu
