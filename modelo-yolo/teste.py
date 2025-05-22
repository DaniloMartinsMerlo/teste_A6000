from ultralytics import YOLO
import cv2
import os

# Carregue o modelo treinado
model = YOLO("best.pt")

# Caminho para imagens de teste (pode ser pasta ou imagem)
image_dir = "test.jpeg"

while True:
    results = model.predict(source=image_dir, conf=0.25, save=True)

    # Pegue a imagem com anotações (renderizada)
    rendered = results[0].plot()

    # Mostra a imagem em uma janela
    cv2.imshow("Detecção", rendered)
    key = cv2.waitKey(0)

    if key == 27:
        break

cv2.destroyAllWindows()
