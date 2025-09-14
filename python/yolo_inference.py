import os
from ultralytics import YOLO
import cv2
import numpy as np
import base64

# Путь к модели относительно корня проекта
model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models/weights/best.pt")
model = YOLO(model_path)

def process_image(file_bytes):
    nparr = np.frombuffer(file_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    results = model(img)
    annotated_img = results[0].plot()

    _, buffer = cv2.imencode('.jpg', annotated_img)
    img_base64 = base64.b64encode(buffer).decode('utf-8')

    objects = []
    for box in results[0].boxes.data.tolist():
        objects.append({
            "bbox": box[:4],
            "confidence": float(box[4]),
            "class": model.names[int(box[5])]
        })

    return img_base64, objects
