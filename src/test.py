from reid_pipeline import Pipeline
from server.milvus_helpers import MilvusHelper

import numpy as np
import cv2

import glob
import time

def test_pipeline():
    pipeline = Pipeline()
    imgs=[]
    img_paths = glob.glob("/home/aistudio/data/data237899/BikePerson/cam_1_2/Bike/Person_00*/cam1_bike_*.jpg")
    start = time.time()
    for img_path in img_paths:
        imgs.append(cv2.imread(img_path))
    cnt_obj=0
    for img in imgs:
        objs = pipeline(img)
        cnt_obj+=len(objs)
    end = time.time()
    num_img = len(imgs)
    time_cost = end - start
    average_time_cost = time_cost / num_img
    print("Number of Image: %d  Number of object: %d  Time Cost: %.4fs Average Time Cost: %.4fs"%(num_img, cnt_obj, time_cost, average_time_cost))

    for obj in objs:
        print(obj)
        #if obj.cls_id == 1:  
            #cv2.imwrite("cyka.jpg",obj.bike_person_img)

def test_main():
    pipeline = Pipeline()

def test_milvus():
    helper = MilvusHelper()
    helper.create_collection("test")
    helper.create_index("test")
    helper.insert(np.random.rand(2048), "test")
    

if __name__ == "__main__":
    test_pipeline()