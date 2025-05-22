from ultralytics import YOLO

model = YOLO('yolo12m.pt')

model.train(
    data='data.yaml',
    epochs= 140,
    imgsz= 512,
    device=0, 
    lr0=0.005
)
