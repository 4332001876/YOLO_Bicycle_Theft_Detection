from reid_pipeline import Pipeline
from server.milvus_helpers import MilvusHelper
from server.mysql_helpers import MySQLHelper

import numpy as np
import cv2

import glob
import time

def get_imgs(path_pattern):
    imgs=[]
    img_paths = glob.glob(path_pattern)
    for img_path in img_paths:
        imgs.append(cv2.imread(img_path))
    return imgs

class Tester:
    def __init__(self, has_pipeline = True) -> None:
        if has_pipeline:
            self.pipeline = Pipeline()
        else:
            self.pipeline = None

    def test_pipeline(self):
        cam_id = 0
        # imgs = get_imgs("/home/aistudio/data/data237899/BikePerson/cam_1_2/Bike/Person_00*/cam1_bike_*.jpg")
        imgs=get_imgs(r"D:\Python\Great Project\YOLO_Bicycle_Theft_Detection_Attachment\BikePerson\cam_1_2\Bike\Person_0000\cam1_bike_*.jpg")

        start = time.time()
        cnt_obj=0
        for img in imgs:
            objs = self.pipeline(img, cam_id=cam_id)
            cnt_obj+=len(objs)
        end = time.time()
        num_img = len(imgs)
        if num_img == 0:
            time_cost = end - start
            average_time_cost = time_cost / num_img
            print("Number of Image: %d  Number of object: %d  Time Cost: %.4fs Average Time Cost: %.4fs"%(num_img, cnt_obj, time_cost, average_time_cost))

        for obj in objs:
            print(obj)
            #if obj.cls_id == 1:  
                #cv2.imwrite("cyka.jpg",obj.bike_person_img)

    def test_milvus(self):
        helper = MilvusHelper()
        helper.create_collection("test")
        helper.create_index("test")
        for _ in range(10):
            embedding = np.array([(i%5)/10.0 for i in range(2048)], dtype=np.float32)# np.random.rand(2048)
            helper.insert_new_bike("test", embedding)

    def clear_milvus(self):
        helper = MilvusHelper("test")
        helper.collection.drop()

    def test_pipeline_to_milvus(self, person_id=0):
        cam_id = 0
        helper = MilvusHelper("test")
        path_pattern=r"D:\Python\Great Project\YOLO_Bicycle_Theft_Detection_Attachment\BikePerson\cam_1_2\Bike\Person_%04d\cam*_bike_*.jpg"%person_id
        imgs = get_imgs(path_pattern)
        print("Number of Images: ", len(imgs))
        
        '''
        if helper.get_num_entities()>0:
            helper.collection.drop()
            helper.create_collection()
            helper.create_index()'''
        
        for img in imgs:
            objs = self.pipeline(img, cam_id=cam_id)
            # print("Number of Objects: ", len(objs))
            for obj in objs:
                if (obj.cls_id == 1):
                    print("insert new bike")
                    id = helper.insert_new_bike(obj.embedding)
                    print("id: ", id)
        
        print('Number of data in collection:', helper.get_num_entities())
        return helper.get_num_entities()
    
    def test_accuracy(self):
        self.clear_milvus()
        num_entities=[]
        for i in range(10):
            num_entities.append(self.test_pipeline_to_milvus(i))
            print("num_entities: ", num_entities)

    def test_mysql(self):
        mysql = MySQLHelper()
        mysql.create_mysql_table("test")


if __name__ == "__main__":
    tester = Tester(has_pipeline=False)
    tester.test_mysql()
