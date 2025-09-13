from flask import Blueprint, jsonify
from models.user import User

users_bp = Blueprint('users', __name__)

# Моковые данные
fake_users = [
    User(1, "Alice", "alice@example.com").to_dict(),
    User(2, "Bob", "bob@example.com").to_dict()
]

@users_bp.route('/', methods=['GET'])
def get_users():
    return jsonify(fake_users)

@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((u for u in fake_users if u['id'] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404
