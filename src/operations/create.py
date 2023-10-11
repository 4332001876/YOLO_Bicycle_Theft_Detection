from server.config import DEFAULT_TABLE

#mivus,mysql根据输入表名创建表，并建立索引

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