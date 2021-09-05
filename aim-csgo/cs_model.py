import torch
from models.experimental import attempt_load

device = 'cuda' if torch.cuda.is_available() else 'cpu'
half = device != 'cpu'

weights=r'D:\yolov5\aim-csgo\models\aim-csgo2.pt'
imgsz=640

def load_model():
    model = attempt_load(weights, map_location=device)  # load FP32 model
    if half:
        model.half()  # to FP16

    if device != 'cpu':
        model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))

    return model
#模型载入