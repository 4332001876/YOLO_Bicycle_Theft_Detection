from server.config import *
from server.logs import LOGGER
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility


class MilvusHelper:
    def __init__(self):
        self.collection = None
        connections.connect(host=MILVUS_HOST, port=MILVUS_PORT)

    def set_collection(self, collection_name):
        if self.has_collection(collection_name):
            self.collection = Collection(name=collection_name)
  
    def has_collection(self, collection_name):
        return utility.has_collection(collection_name)


    def create_collection(self, collection_name):
        # Create milvus collection if not exists
        if not self.has_collection(collection_name):
                
            bicycle_id = FieldSchema(name="bicycle_id",
                                    dtype=DataType.INT64,
                                    descrition="the only id for every bike-person pair",
                                    is_primary=True,
                                    auto_id=True)
                
            bicycle_embedding = FieldSchema(name="bicycle_embedding", 
                                            dtype=DataType.FLOAT_VECTOR, 
                                            descrition="float bicycle_embedding",
                                            dim=VECTOR_DIMENSION,
                                            is_primary=False,
                                            auto_id = False)
                
            schema = CollectionSchema(fields = [bicycle_id,
                                                bicycle_embedding], 
                                                description="bicycle search")
                
            self.collection = Collection(name=collection_name, schema=schema)
        else:
            self.set_collection(collection_name)
            return "OK"
        
    def create_index(self, collection_name):
        # Create IVF_FLAT index on milvus collection
        self.set_collection(collection_name)
        if self.collection.has_index():
            return None
        default_index = {"index_type": "IVF_FLAT", "metric_type": METRIC_TYPE, "params": {"nlist": 16384}}
        status = self.collection.create_index(field_name="bicycle_embedding", index_params=default_index, timeout=60)
        return status
        

    def search_vectors(self, collection_name, vectors, top_k):
        # Search vector in milvus collection
        self.set_collection(collection_name)
        search_params = {"metric_type": METRIC_TYPE, "params": {"nprobe": 16}}
        res = self.collection.search(vectors, anns_field="bicycle_embedding", param=search_params, limit=top_k)
        return res 
        # res[0].ids:get the IDs of all returned hits
        # res[0].distances:get the distances to the query vector from all returned hits

    def count(self, collection_name):
        self.set_collection(collection_name)
        num = self.collection.num_entities
        return num

        
    def delete_collection(self, collection_name):
        self.set_collection(collection_name)
        self.collection.drop()
        return "ok"

        
    

    def insert_new_bike(self, collection_name, bicycle_embedding):#TODO:maybe还要改
        # 自行车embedding逐条插入数据库，先在milvus里面检索top1,如果与top1的相似度大于阈值，就不插入，否则插入
        self.set_collection(collection_name)
        
        search_result = self.search_vectors(collection_name, [bicycle_embedding], 1)
        if(search_result[0].distances[0] >= DISTANCE_THERSHOLD):
            return -1
        else:
            mr = self.collection.insert(bicycle_embedding)
            id = mr.primary_keys
            self.collection.load()
            LOGGER.debug(
                f"Insert vector to Milvus in collection: {collection_name} with one new row")
            return id