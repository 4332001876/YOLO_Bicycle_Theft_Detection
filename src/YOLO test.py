from ultralytics import YOLO
import cv2
import time

# Load a segmentation model
model = YOLO("yolov8n-seg.pt")  
results=model(source="../testcases/test_mid_autumn_party.jpg", show=True,save=True)

for result in results:
    print(result)
    boxes = result.boxes  # Boxes object for bbox outputs
    masks = result.masks  # Masks object for segmentation masks outputs
    probs = result.probs  # Class probabilities for classification outputs

res_plotted = results[0].plot()
cv2.imshow("result", res_plotted)

key = cv2.waitKey(0)
