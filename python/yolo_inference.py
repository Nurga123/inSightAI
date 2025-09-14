import os
from ultralytics import YOLO
import cv2
import numpy as np
import base64

# Путь к модели
model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models/weights/best.pt")
model = YOLO(model_path)

def process_image(file_bytes):
    # Декодируем изображение из байтов
    nparr = np.frombuffer(file_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Инференс
    results = model.predict(img, save=False)

    # Получаем аннотированное изображение
    annotated_img = results[0].plot()  # numpy array (RGB)

    # Конвертируем в BGR для OpenCV, если нужно
    annotated_img_bgr = cv2.cvtColor(annotated_img, cv2.COLOR_RGB2BGR)

    # Кодируем в base64
    _, buffer = cv2.imencode('.jpg', annotated_img_bgr)
    img_base64 = base64.b64encode(buffer).decode('utf-8')

    # Формируем список объектов
    objects = []
    for box in results[0].boxes.data.tolist():
        objects.append({
            "bbox": [float(x) for x in box[:4]],
            "confidence": float(box[4]),
            "class": model.names[int(box[5])]
        })

    return img_base64, objects
