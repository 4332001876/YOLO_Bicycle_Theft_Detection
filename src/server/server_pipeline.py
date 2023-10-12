from config import *
from reid_pipeline import Pipeline, DetectedObject
from milvus_helpers import MilvusHelper
from mysql_helpers import MySQLHelper

import random


# *? 该文件实现数据库的创建，插入，搜索，按时删除等功能
# |   0   |     1      |     2     |     3      |    4     |       5       |    6     |
# | :---: | :--------: | :-------: | :--------: | :------: | :-----------: | :------: |
# |  id   | bicycle_id | camera_id | start_time | end_time | location_desc | img_path |

class ServerPipeline:
    def __init__(self) -> None:
        self.pipeline = Pipeline()
        self.milvus = MilvusHelper(MILVUS_DB_NAME)
        self.mysql = MySQLHelper()
        self.mysql.create_mysql_table(MYSQL_TABLE)
    
    def insert_new_data_from_img(self, img, cam_id):
        if random.random() > 0.9999:
            self.mysql.auto_delete_ExpiredData(MYSQL_TABLE, delete_interval=MYSQL_DELETE_INTERVAL)
        objs = self.pipeline(img, cam_id=cam_id)
        for obj in objs:
            if obj.cls_id == 1:  
                bike_id = self.milvus.insert_new_bike(obj.embedding)
                self.insert_bike_occurrence(bike_id, obj)

    def insert_bike_occurrence(self, bike_id, obj: DetectedObject):
        bike_occurrence_res = self.get_bike_occurrence([obj], top_k=1)
        single_bike_occurrence_res = None
        for res in bike_occurrence_res.values():
            single_bike_occurrence_res = res
        single_bike_occurrence_dict = self.mysql.db_line_to_dict(single_bike_occurrence_res[0])
        if obj.cam_id == single_bike_occurrence_dict["camera_id"]:
            self.mysql.update_end_time(MYSQL_TABLE, single_bike_occurrence_dict["id"], obj.end_time)
        else:
            self.mysql.insert(MYSQL_TABLE, bike_id, obj)

    def query_img(self, img, cam_id, top_k=10):
        objs = self.pipeline(img, cam_id=cam_id)
        bike_occurrence_res = self.get_bike_occurrence(objs, top_k)
        

    def get_bike_occurrence(self, objs, top_k=10):
        bike_occurrence_res = {}
        for obj in objs:
            if obj.cls_id == 1: 
                search_result = self.milvus.search_vectors(obj.embedding, top_k)
                for res in search_result:
                    bike_id = res.ids[0]
                    bike_occurrence_res[bike_id] = self.mysql.search_by_bicycle_id(bike_id, MYSQL_TABLE)
        return bike_occurrence_res
    
    def bike_occurrence_res_to_str(self, bike_occurrence_res:dict):
        for single_bike_occurrence_res in bike_occurrence_res.values():
            for db_line in single_bike_occurrence_res:
                self.mysql.db_line_to_str(db_line)
    
    def count_bike(self):
        if not self.milvus.has_collection():
            return 0
        return self.milvus.get_num_entities()



