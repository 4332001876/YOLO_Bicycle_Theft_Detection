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


## 数据库结构



### MySQL
|   0   |     1      |     2     |     3      |    4     |       5       |    6     |
| :---: | :--------: | :-------: | :--------: | :------: | :-----------: | :------: |
|  id   | bicycle_id | camera_id | start_time | end_time | location_desc | img_path |



|     Field     |        Type         | Null  |  Key  | Default |     Extra      |
| :-----------: | :-----------------: | :---: | :---: | :-----: | :------------: |
|      id       | bigint(20) unsigned |  NO   |  PRI  |  NULL   | auto_increment |
|  bicycle_id   | bigint(20) unsigned |  YES  |  MUL  |  NULL   |                |
|   camera_id   |  int(10) unsigned   |  YES  |       |  NULL   |                |
|  start_time   |     bigint(20)      |  YES  |       |  NULL   |                |
|   end_time    |     bigint(20)      |  YES  |       |  NULL   |                |
| location_desc |     varchar(50)     |  YES  |       |  NULL   |                |
|   img_path    |    varchar(100)     |  YES  |       |  NULL   |                |
