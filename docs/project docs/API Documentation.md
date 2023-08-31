# API文档

## 项目结构

- run: 启动整个程序运行的逻辑，包括通过服务器提供服务、训练、测试、评估等
- reid_pipeline: Re-id流程主体逻辑
- models: 模型具体实现，包括各模型和用于管理模型的类
- database_manager: 数据库管理，包括数据增删查改等
- utils: 工具类，包括各种工具函数、工具类


## 基本API

### run


### reid_pipeline
#### pipeline.py
```python
class Pipeline:
    def __init__(self):
        pass
    def __call__(self, *args, **kwargs):
        pass
    def spot_object_from_image(self, image):
        pass
    def spot_object_from_video(self, video):
        pass
    def get_embedding(self, objects):
        pass
    def submit_result(self, embeddings):
        pass

```

#### reid_data_manager.py
```python
class BikePersonObject:
    def __init__(self, id, image, bbox, embedding):
        pass


```





