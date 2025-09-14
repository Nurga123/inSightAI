from ultralytics import YOLO
import os

# Загружаем модель один раз
model = YOLO("models/weights/best.pt")

def process_image(file_bytes):
    """
    file_bytes — это байты изображения из запроса
    Возвращает (путь к изображению с боксами, список найденных объектов)
    """

    temp_input = "temp_input.jpg"
    with open(temp_input, "wb") as f:
        f.write(file_bytes)

    results = model(temp_input)

    annotated_img_path = "annotated.jpg"
    results[0].plot(save=True)
    
    os.rename("runs/detect/exp/annotated.jpg", annotated_img_path)

    
    objects = []
    for box in results[0].boxes.data.tolist():  # [x1, y1, x2, y2, score, class]
        objects.append({
            "bbox": box[:4],
            "confidence": box[4],
            "class": model.names[int(box[5])]
        })

    return annotated_img_path, objects
