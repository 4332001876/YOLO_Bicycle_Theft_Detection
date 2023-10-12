import sys
sys.path.append('..')
from config import *
import server.image_utils as image_utils

# *！id,bicycle_id,camera_id,feature,start_time,end_time

# *? 该文件实现数据库的创建，插入，搜索，按时删除等功能


def do_create(table, milvus, mysql):
    table_name = table
    if not table_name:
        table_name = MYSQL_TABLE
    mysql.create_mysql_table(table_name)
    milvus.create_collection(table_name)
    milvus.create_index(table_name)
    


def get_last_endtime_data(mysql_bicycle_res):
    #获取每种camera_id下最后一次endtime的数据
    last_endtime_data = {}
    for res in mysql_bicycle_res:
        camera_id = res[2]#3号字段为camera_id
        end_time = res[5]#6号字段为end_time
        if camera_id not in last_endtime_data or end_time > last_endtime_data[camera_id][5]:
            last_endtime_data[camera_id] = res
    return last_endtime_data

def check_camera_id_exist(last_data, camera_id):
    #在last_data里查找指定camera_id的数据是否存在
    for data in last_data:
        if data[2] == camera_id:
            return data
    return False


#TODO: data定义有点紊乱，需要reid_pipeline的embedding输出
def do_insert(table_name,milvus, mysql,data):
    if not table_name:
        table_name = MYSQL_TABLE

    #从milvus里检索该自行车向量是否存在，如果存在，返回bicycle_id;若否,则在milvus里插入并返回新id
    bicycle_embedding = get_embedding(data)
    bicycle_id = milvus.insert_new_bicycle(MILVUS_TABLE,bicycle_embedding).id
    #在mysql里插入该自行车信息
    mysql_bicycle_res = mysql.serach_by_bicycle_id(bicycle_id,table_name)
    if len(mysql_bicycle_res) == 0:
        mysql.insert(table_name, data)
    else:
        last_data = get_last_endtime_data(mysql_bicycle_res)
        if check_camera_id_exist == False:
            mysql.insert(table_name, data)
        else:
            if(data.start_time > check_camera_id_exist[5]):
                mysql.insert(table_name, data)
            elif(data.start_time > check_camera_id_exist[4] and data.end_time < check_camera_id_exist[]):
                data.end_time = data.end_time
                mysql.update(table_name, data)



def do_delete(id, table_name, milvus, mysql):
    if not table_name:
        table_name = MYSQL_TABLE
    # 删除原有milvus 数据
    ms_data = mysql.search_by_ids([id], table_name)
    if len(ms_data) == 0:
        raise Exception("id not exist")
    milvus.delete(table_name, "id in [%s]" % ms_data[0][1])
    mysql.delete_by_id(table_name, id)
    return "ok"


def do_count(table_name, milvus):
    if not table_name:
        table_name = MYSQL_TABLE
    if not milvus.has_collection(table_name):
        return None
    num = milvus.count(table_name)
    return num