from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
import os

app = Flask(__name__)

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASS = os.getenv("MONGO_PASS")
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = os.getenv("MONGO_PORT")
MONGO_DB   = os.getenv("MONGO_DB")

MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}?authSource=admin"
print("Conected em:", MONGO_URI)

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
colecao = db["users"]

def serialize_doc(doc):
    return {**doc, "_id": str(doc["_id"])}

@app.route("/")
def home():
    return jsonify({"message": "API Flask + MongoDB UP"})

@app.route("/users", methods=["POST"])
def criar_usuario():
    dados = request.get_json()
    resultado = colecao.insert_one(dados)
    return jsonify({"id": str(resultado.inserted_id)}), 201

@app.route("/users", methods=["GET"])
def listar_users():
    users = list(colecao.find())
    return jsonify([serialize_doc(u) for u in users])

@app.route("/users/<id>", methods=["GET"])
def buscar_usuario(id):
    usuario = colecao.find_one({"_id": ObjectId(id)})
    if usuario:
        return jsonify(serialize_doc(usuario))
    return jsonify({"error": "User not found"}), 404

@app.route("/users/<id>", methods=["PUT"])
def atualizar_usuario(id):
    dados = request.get_json()
    resultado = colecao.update_one({"_id": ObjectId(id)}, {"$set": dados})
    if resultado.matched_count > 0:
        return jsonify({"message": "User updated successfully"})
    return jsonify({"error": "User not found"}), 404

@app.route("/users/<id>", methods=["DELETE"])
def deletar_usuario(id):
    resultado = colecao.delete_one({"_id": ObjectId(id)})
    if resultado.deleted_count > 0:
        return jsonify({"message": "User deleted successfully"})
    return jsonify({"error": "User not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
