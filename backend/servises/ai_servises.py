def detect_car_status(image_url: str) -> dict:
    """
    Моковая функция ИИ для детекции состояния машины.
    В реальном проекте здесь будет модель ML/AI.
    """
    if "dirty" in image_url:
        status = "dirty"
    elif "broken" in image_url:
        status = "broken"
    elif "worn" in image_url:
        status = "worn"
    else:
        status = "ok"
    
    return {"image_url": image_url, "detected_status": status}
