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
其支持的输入类型很多，详情可查看：https://docs.ultralytics.com/modes/predict/#inference-sources


## 处理YOLO输出结果
### 获得结果各部分
```python
from ultralytics import YOLO

# Load a model
model = YOLO('yolov8n.pt')  # pretrained YOLOv8n model

# Run batched inference on a list of images
results = model(['im1.jpg', 'im2.jpg'], stream=True)  # return a generator of Results objects

# Process results generator
for result in results:
    boxes = result.boxes  # Boxes object for bbox outputs
    masks = result.masks  # Masks object for segmentation masks outputs
    keypoints = result.keypoints  # Keypoints object for pose outputs
    probs = result.probs  # Probs object for classification outputs
```
可以看到，模型输出结果返回Results对象的列表，Results对象包含了boxes、masks、keypoints、probs四个对象（当然还有其它属性），分别对应了检测框、分割区域、所处位置、置信度。

### 结果处理
可直接参考：https://docs.ultralytics.com/modes/predict/#working-with-results
```python

```






## YOLO训练数据集汇总
- https://bair.berkeley.edu/blog/2018/05/30/bdd/
- https://www.kaggle.com/datasets/dataclusterlabs/bicycle-image-dataset-vehicle-dataset