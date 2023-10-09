from ..server.config import DEFAULT_TABLE
import pickle
import base64
#! copy自别人的项目，急需适配修改！！！

def do_load(table, milvus_client, mysql_cli):
    """
    循环调用上传
    :param table:
    :param milvus_client:
    :param mysql_cli:
    :return:
    """
    table_name = table
    if not table_name:
        table_name = DEFAULT_TABLE
    while True:
        do_load_once(table_name, milvus_client, mysql_cli)


def do_load_once(table_name, milvus_client, mysql_cli):
    """
    调用一次更新
    将特征更新到milvus中
    :param table_name:
    :param milvus_client:
    :param mysql_cli:
    :return:
    """
    #  0     1       2     3     4
    # id,milvus_id,tags,brief,feature
    ms_data = mysql_cli.search_by_update_status(table_name, 0, 100)#search_by_update_status(self, table_name, upload_status, limit)
    if len(ms_data) == 0:
        raise Exception("ok")
    ids = []
    for item in ms_data:
        try:
            if item[1] is not None:
                milvus_client.delete(table_name, "id in [%s]" % item[1])
            feat = base64.b64encode(pickle.dumps(item[4])).decode()
            ids = milvus_client.insert(table_name, [feat])
            mysql_cli.update_status(table_name, (ids[0], 1, item[0]))
        except Exception as e:
            if len(ids) > 0:
                milvus_client.delete(table_name, "id in [%s]" % ids[0])
            raise e
        
'''
函数的主要功能是将数据加载到Milvus中。首先，它会检查table的值是否为空，如果为空，则使用名为DEFAULT_TABLE的默认表。

然后，函数进入一个无限循环，不断调用do_load_once函数来上传数据。

在每次调用do_load_once函数时，首先通过调用mysql_cli的search_by_update_status方法，从MySQL数据库中获取需要更新的数据。获取到的数据存储在ms_data变量中。

如果ms_data的长度为0，即没有需要更新的数据，函数会引发异常。

接下来，函数遍历ms_data，对每条数据进行处理。如果数据的第一个字段item[1]不为空，即已经在Milvus中存在与该数据关联的记录，则使用milvus_client的delete方法删除这些记录。

然后，函数使用pickle库将数据的第五个字段序列化，并使用base64库对序列化结果进行编码，得到特征feat。

接着，函数使用milvus_client的insert方法将特征插入Milvus，并将返回的插入ID存储在ids列表中。

最后，函数调用mysql_cli的update_status方法，更新数据的状态，将Milvus插入ID、更新状态和数据的第一个字段作为参数传递。

如果在上述过程中出现异常，函数会首先判断ids列表的长度是否大于0，如果是，则使用milvus_client的delete方法根据Milvus插入ID删除记录。然后，函数重新引发捕获到的异常。

总体而言，do_load函数不断地调用do_load_once函数来更新数据到Milvus中，直到没有需要更新的数据为止。
'''