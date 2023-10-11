from reid_pipeline import Pipeline
from server.milvus_helpers import MilvusHelper

import numpy as np

def test_pipeline():
    pipeline = Pipeline()

def test_main():
    pipeline = Pipeline()

def test_milvus():
    helper = MilvusHelper()
    helper.create_collection("test")
    helper.create_index("test")
    helper.insert(np.random.rand(2048), "test")
    

if __name__ == "__main__":
    test_milvus()

