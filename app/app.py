"""Flask application to manage MongoDB data."""
import os
from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASS = os.getenv("MONGO_PASS")
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = os.getenv("MONGO_PORT")
MONGO_DB   = os.getenv("MONGO_DB")

MONGO_URI = (
    f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/"
    f"{MONGO_DB}?authSource=admin"
)

print("Conected em:", MONGO_URI)

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
colecao = db["users"]


"""Module init"""
def serialize_doc(doc):
    """Module doc"""
    return {**doc, "_id": str(doc["_id"])}

@app.route("/")
def home():
    """Module Init app API Flask + MongoDB UP """
    return jsonify({"message": "API Flask + MongoDB UP"})

@app.route("/users", methods=["POST"])
def create_user():
    """Create user"""
    dados = request.get_json()
    resultado = colecao.insert_one(dados)
    return jsonify({"id": str(resultado.inserted_id)}), 201

@app.route("/users", methods=["GET"])
def list_users():
    """List users"""
    users = list(colecao.find())
    return jsonify([serialize_doc(u) for u in users])

@app.route("/users/<user_id>", methods=["GET"])
def list_user_by_id(user_id):
    """Get user by {user_id}"""
    user = colecao.find_one({"_id": ObjectId(user_id)})
    if user:
        return jsonify(serialize_doc(user))
    return jsonify({"error": "User not found"}), 404

@app.route("/users/<user_id>", methods=["PUT"])
def update_user_by_id(user_id):
    """Update user by {user_id}"""
    dados = request.get_json()
    resultado = colecao.update_one({"_id": ObjectId(user_id)}, {"$set": dados})
    if resultado.matched_count > 0:
        return jsonify({"message": "User updated successfully"})
    return jsonify({"error": "User not found"}), 404

@app.route("/users/<user_id>", methods=["DELETE"])
def delete_user_by_id(user_id):
    """Delete user by {user_id}"""
    resultado = colecao.delete_one({"_id": ObjectId(user_id)})
    if resultado.deleted_count > 0:
        return jsonify({"message": "User deleted successfully"})
    return jsonify({"error": "User not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
