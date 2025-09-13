ffrom flask import Blueprint, request, jsonify
from models.car import Car
from services.ai_service import detect_car_status

cars_bp = Blueprint('cars', __name__)

# Моковые данные машин
fake_cars = [
    Car(1, "Toyota Camry", "ok").to_dict(),
    Car(2, "Honda Civic", "dirty").to_dict(),
    Car(3, "BMW X5", "broken").to_dict()
]

@cars_bp.route('/', methods=['GET'])
def get_cars():
    return jsonify(fake_cars)

@cars_bp.route('/detect', methods=['POST'])
def detect_car():
    data = request.json
    image_url = data.get('image_url')
    if not image_url:
        return jsonify({"error": "No image provided"}), 400
    
    result = detect_car_status(image_url)
    return jsonify(result)
