# YOLO Quick Start
## 安装YOLO
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple ultralytics

建议安装：
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple opencv-python

## 最简单的实例
```python
from ultralytics import YOLO

# Load a segmentation model
model = YOLO("yolov8n-seg.pt")  
#也可以下载好模型，然后把模型路径塞进去，model=YOLO("D:/Python/Great Project/YOLO_Bicycle_Theft_Detection/src/yolov8n-seg.pt")
# 注意路径名若用反斜杠要加转义符：\ x \\ √
results=model(source="../testcases/test_mid_autumn_party.jpg", show=True,save=True)
```


