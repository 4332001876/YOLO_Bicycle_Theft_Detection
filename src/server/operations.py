#  0     1         2             3                     4
# id,milvus_id,bicycle_id,location_description,feature
import sys
sys.path.append('..')
from config import *
import server.image_utils as image_utils
# *? 该文件实现数据库的创建，插入，搜索，按时删除等功能


def do_create(table, milvus_client, mysql_cli):
    table_name = table
    if not table_name:
        table_name = DEFAULT_TABLE
    try:
        mysql_cli.create_mysql_table(table_name)
        milvus_client.create_collection(table_name)
        milvus_client.create_index(table_name)
    except Exception as e:
        raise e
    

#TODO:下面这两个函数貌似没用...
#将 MySQL 数据库中未上传的特征数据更新到 Milvus 中
def do_load(table, milvus_client, mysql_cli):
    table_name = table
    if not table_name:
        table_name = DEFAULT_TABLE
    while True:
        do_load_once(table_name, milvus_client, mysql_cli)

def do_load_once(table_name, milvus_client, mysql_cli):
    ms_data = mysql_cli.search_by_update_status(table_name, 0, 10)#一次读入10条
    if len(ms_data) == 0:
        raise Exception("ok")
    ids = []
    for item in ms_data:
        try:
            if item[1] is not None:
                milvus_client.delete(table_name, "id in [%s]" % item[1])
            feature = image_utils.obj_decode(item[4])
            ids = milvus_client.insert(table_name, [feature])
            mysql_cli.update_status(table_name, (ids[0], 1, item[0]))
        except Exception as e:
            if len(ids) > 0:
                milvus_client.delete(table_name, "id in [%s]" % ids[0])
            raise e


#TODO: search的
def do_search(table_name, img_path, top_k, milvus_client, mysql_cli):
    if not table_name:
        table_name = DEFAULT_TABLE
    feature= get_embedding(img_path)
    vectors = milvus_client.search_vectors(table_name, [feature], top_k)
    res = []
    if len(vectors[0]) == 0:
        return []
    vectors_dict = {}
    for x in vectors[0]:
        vectors_dict[x.id] = x.distance
    paths = mysql_cli.search_by_milvus_ids(list(vectors_dict.keys()), table_name)

    for i in range(len(paths)):
        data = {}
        data['id'] = paths[i][0]
        data['bicycle_id'] = paths[i][2]
        data['location_description'] = paths[i][3]
        data['distance'] = vectors_dict.get(int(paths[i][1]))
        res.append(data)
    return res




def do_delete(id, table_name, milvus_cli, mysql_cli):
    if not table_name:
        table_name = DEFAULT_TABLE
    # 删除原有milvus 数据
    ms_data = mysql_cli.search_by_ids([id], table_name)
    if len(ms_data) == 0:
        raise Exception("id not exist")
    milvus_cli.delete(table_name, "id in [%s]" % ms_data[0][1])
    mysql_cli.delete_by_id(table_name, id)
    return "ok"


def do_count(table_name, milvus_cli):
    if not table_name:
        table_name = DEFAULT_TABLE
    if not milvus_cli.has_collection(table_name):
        return None
    num = milvus_cli.count(table_name)
    return num