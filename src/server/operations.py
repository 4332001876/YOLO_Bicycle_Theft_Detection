import pickle
import base64
from config import *
from milvus_helpers import MilvusHelper as milvus
from mysql_helpers import MySQLHelper as mysql


# *? 该文件实现数据库的创建，插入，搜索，按时删除等功能
# *！0 |     1    |     2   |   3   |    4     |   5
# *！id,bicycle_id,camera_id,feature,start_time,end_time

#! 下面需要改写成一个db_pipeline类，完成流水线操作
def do_create(milvus, mysql):
    mysql.create_mysql_table(MYSQL_TABLE)
    milvus.create_collection()
    milvus.create_index()
    return "ok"
#---------------------------------------------------------------------------------------------------
#mysql不能直接存储图片信息，下面是两个函数用于将图片信息转化为字符串存储，以及从字符串转化为图片信息
def obj_encode(obj_image):
    return base64.b64encode(pickle.dumps(obj_image)).decode() 

def obj_decode(objStr):
    return pickle.loads(base64.b64decode(objStr))

#承接reid_pipeline的输出，格式转化为Mysql的输入
def TransformData(DetectedObject):
    #data: [id, bicycle_id,camera_id, feature, start_time, end_time]
    formated_data = []
    
    #TODO：这部分还没写完....
    return formated_data

#---------------------------------------------------------------------------------------------------
def get_last_endtime_data(mysql_bicycle_res):# *下面do_insert的子函数
    #获取每种camera_id下最后一次endtime的数据
    last_endtime_data = {}
    for res in mysql_bicycle_res:
        camera_id = res[2]#3号字段为camera_id
        end_time = res[5]#6号字段为end_time
        if camera_id not in last_endtime_data or end_time > last_endtime_data[camera_id][5]:
            last_endtime_data[camera_id] = res
    return last_endtime_data

def check_camera_id_exist(last_data, camera_id):#* 下面do_insert的子函数
    #在last_data里查找指定camera_id的数据是否存在
    for data in last_data:
        if data[2] == camera_id:
            return data
    return False

#TODO: 这里data定义有点紊乱，需要reid_pipeline的embedding输出
def do_insert(table_name,milvus, mysql,data):
    if not table_name:
        table_name = MYSQL_TABLE

    #从milvus里检索该自行车向量是否存在，如果存在，返回bicycle_id;若否,则在milvus里插入并返回新id
    bicycle_embedding = get_embedding(data)
    bicycle_id = milvus.insert_new_bicycle(MILVUS_TABLE,bicycle_embedding).id
    #在mysql里插入该自行车信息
    mysql_bicycle_res = mysql.serach_by_bicycle_id(bicycle_id,table_name)
    if len(mysql_bicycle_res) == 0:#若mysql里也没有这条记录，则插入mysql
        mysql.insert(table_name, data)
    else:
        last_data = get_last_endtime_data(mysql_bicycle_res)
        if check_camera_id_exist == False:
            mysql.insert(table_name, data)
        else:
            if(data.start_time > check_camera_id_exist[5]):
                mysql.insert(table_name, data)
            elif(data.start_time > check_camera_id_exist[4] and data.end_time < check_camera_id_exist[4]):
                data.end_time = data.end_time
                mysql.update(table_name, data)

#---------------------------------------------------------------------------------------------------
# *? 对用户展示搜索结果，从mysql里返回所有记录
def show_search(table_name,milvus,mysql,bicycle_embedding):
    if not table_name:
        table_name = MYSQL_TABLE
    bicycle_id = milvus.check_bicycle_exist(bicycle_embedding)
    if bicycle_id == False:
        return None
    else:
        mysql_bicycle_res = mysql.search_by_bicycle_id(bicycle_id,table_name)
        return mysql_bicycle_res
        
#---------------------------------------------------------------------------------------------------
def do_delete(id, table_name, milvus, mysql):
    #TODO：实现定期删除功能
    if not table_name:
        table_name = MYSQL_TABLE
    # 删除原有milvus 数据
    ms_data = mysql.search_by_ids([id], table_name)
    if len(ms_data) == 0:
        raise Exception("id not exist")
    milvus.delete(table_name, "id in [%s]" % ms_data[0][1])
    mysql.delete_by_id(table_name, id)
    return "ok"

#---------------------------------------------------------------------------------------------------
def do_count(table_name, milvus):
    if not table_name:
        table_name = MYSQL_TABLE
    if not milvus.has_collection(table_name):
        return None
    num = milvus.count(table_name)
    return num