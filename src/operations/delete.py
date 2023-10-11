from server.config import DEFAULT_TABLE

def do_delete(id, table_name, milvus_cli, mysql_cli):
    if not table_name:
        table_name = DEFAULT_TABLE
    # 删除原有milvus 数据
    ms_data = mysql_cli.search_by_ids([id], table_name)
    if len(ms_data) == 0:
        raise Exception("id not exist")
    milvus_cli.delete(table_name, "id in [%s]" % ms_data[0][1])#!milvus的expr方法，此处仍需改进
    mysql_cli.delete_by_id(table_name, id)
    return "ok"