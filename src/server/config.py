import os

############### Milvus Configuration ###############
MILVUS_HOST = "127.0.0.1"
MILVUS_PORT =  19530
VECTOR_DIMENSION = 2048
METRIC_TYPE = "COSINE"
MILVUS_TABLE = "similarity_search"
TOP_K = 10
INDEX_TYPE = "IVF_FLAT"
DISTANCE_THERSHOLD =  0.992


############### MySQL Configuration ###############
MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PWD = "123456"
MYSQL_TABLE = "Primary_table"
MYSQL_DELETE_INTERVAL = 7 #days

############### Data Path ###############
UPLOAD_PATH = "tmp/search-images"

DATE_FORMAT =  "%Y-%m-%d %H:%M:%S"
