class Car:
    def __init__(self, id, model, status):
        self.id = id
        self.model = model
        self.status = status
    
    def to_dict(self):
        return {"id": self.id, "model": self.model, "status": self.status}
