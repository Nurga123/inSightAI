from ultralytics import YOLO
import os
import shutil

# Загружаем модель один раз при старте
model = YOLO("models/weights/best.pt")  # путь к твоей модели

def process_image(file_bytes):
    """
    file_bytes — это байты изображения из запроса
    Возвращает (путь к изображению с боксами, список найденных объектов)
    """
    # Сохраняем временный входной файл
    temp_input = "temp_input.jpg"
    with open(temp_input, "wb") as f:
        f.write(file_bytes)

    # Запускаем детекцию
    results = model(temp_input)

    # Папка для сохранения результатов
    output_dir = "runs/detect/exp"
    os.makedirs(output_dir, exist_ok=True)

    # Сохраняем аннотированное изображение
    results[0].plot()  # генерируем изображение с бокcами
    results[0].save(save_dir=output_dir)

    # Копируем аннотированное изображение в корень проекта
    annotated_img_path = "annotated.jpg"
    exp_files = os.listdir(output_dir)
    for f in exp_files:
        if f.endswith(".jpg") or f.endswith(".png"):
            shutil.copy(os.path.join(output_dir, f), annotated_img_path)
            break

    # Собираем найденные объекты
    objects = []
    for box in results[0].boxes.data.tolist():  # [x1, y1, x2, y2, confidence, class]
        objects.append({
            "bbox": box[:4],
            "confidence": float(box[4]),
            "class": model.names[int(box[5])]
        })

    return annotated_img_path, objects
