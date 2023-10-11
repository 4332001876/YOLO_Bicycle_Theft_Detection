from server.config import *
from server.logs import LOGGER
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility


class MilvusHelper:
    def __init__(self):
        try:
            self.collection = None
            connections.connect(host=MILVUS_HOST, port=MILVUS_PORT)
            LOGGER.debug(f"Successfully connect to Milvus with IP:{MILVUS_HOST} and PORT:{MILVUS_PORT}")
        except Exception as e:
            LOGGER.error(f"Failed to connect Milvus: {e}")
            # sys.exit(1)
            raise e

    def set_collection(self, collection_name):
        try:
            if self.has_collection(collection_name):
                self.collection = Collection(name=collection_name)
            else:
                raise Exception(f"There is no collection named:{collection_name}")
        except Exception as e:
            LOGGER.error(f"Failed to load data to Milvus: {e}")
            # sys.exit(1)
            raise e

    def has_collection(self, collection_name):
        # Return if Milvus has the collection
        try:
            return utility.has_collection(collection_name)
        except Exception as e:
            LOGGER.error(f"Failed to load data to Milvus: {e}")
            # sys.exit(1)
            raise e

    def create_collection(self, collection_name):
        # Create milvus collection if not exists
        try:
            if not self.has_collection(collection_name):
                
                milvus_id = FieldSchema(name="pair_id",
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
                
                schema = CollectionSchema(fields = [milvus_id,
                                                    bicycle_embedding], 
                                                    description="bicycle search")
                
                self.collection = Collection(name=collection_name, schema=schema)
                LOGGER.debug(f"Create Milvus collection: {collection_name}")
            else:
                self.set_collection(collection_name)
            return "OK"
        except Exception as e:
            LOGGER.error(f"Failed to load data to Milvus: {e}")
            # sys.exit(1)
            raise e
        
    def create_index(self, collection_name):
        # Create IVF_FLAT index on milvus collection
        try:
            self.set_collection(collection_name)
            if self.collection.has_index():
                return None
            default_index = {"index_type": "IVF_FLAT", "metric_type": METRIC_TYPE, "params": {"nlist": 16384}}
            status = self.collection.create_index(field_name="bicycle_embedding", index_params=default_index, timeout=60)
            if not status.code:
                LOGGER.debug(
                    f"Successfully create index in collection:{collection_name} with param:{default_index}")
                return status
            else:
                raise Exception(status.message)
        except Exception as e:
            LOGGER.error(f"Failed to create index: {e}")
            # sys.exit(1)
            raise e
        

    def search_vectors(self, collection_name, vectors, top_k):
        # Search vector in milvus collection
        try:
            self.set_collection(collection_name)
            search_params = {"metric_type": METRIC_TYPE, "params": {"nprobe": 16}}
            # data = [vectors]n
            res = self.collection.search(vectors, anns_field="bicycle_embedding", param=search_params, limit=top_k)
            LOGGER.debug(f"Successfully search in collection: {res}")
            return res 
        except Exception as e:
            LOGGER.error(f"Failed to search vectors in Milvus: {e}")
            # sys.exit(1)
            raise e
        # res[0].ids:get the IDs of all returned hits
        # res[0].distances:get the distances to the query vector from all returned hits

    def count(self, collection_name):
        # Get the number of milvus collection
        try:
            self.set_collection(collection_name)
            num = self.collection.num_entities
            LOGGER.debug(f"Successfully get the num:{num} of the collection:{collection_name}")
            return num
        except Exception as e:
            LOGGER.error(f"Failed to count vectors in Milvus: {e}")
            #  # sys.exit(1)
            raise e
        
    def delete_collection(self, collection_name):
        # Delete Milvus collection
        try:
            self.set_collection(collection_name)
            self.collection.drop()
            LOGGER.debug("Successfully drop collection!")
            return "ok"
        except Exception as e:
            LOGGER.error(f"Failed to drop collection: {e}")
            #  # sys.exit(1)
            raise e
        
    

    def insert_new_bike(self, collection_name, bicycle_embedding):#TODO:maybe还要改
        # 自行车embedding逐条插入数据库，先在milvus里面检索top1,如果与top1的相似度大于阈值，就不插入，否则插入
        self.set_collection(collection_name)
        
        search_result = self.search_vectors(collection_name, [bicycle_embedding], 1)
        if(search_result[0].distances[0] >= DISTANCE_THERSHOLD):
            return -1
        else:
            mr = self.collection.insert([bicycle_embedding])
            id = mr.primary_keys
            self.collection.load()
            LOGGER.debug(
                f"Insert vector to Milvus in collection: {collection_name} with one new row")
            return id