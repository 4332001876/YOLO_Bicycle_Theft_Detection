from ..server.config import DEFAULT_TABLE
from ..server.logs import LOGGER
'''
函数的主要功能是计算给定表中的元素数量，使用了milvus_cli库中的count方法。

函数的第一部分是一个条件判断语句，如果table_name为空，则默认使用名为DEFAULT_TABLE的表。

接下来，该函数会检查是否存在名为table_name的集合/表。如果不存在，则返回None。

然后，该函数调用Milvus客户端的count方法来获取表中元素的数量，并将该数字存储在变量num中。

最后，该函数返回num，或者如果在运行过程中遇到了错误，则记录错误并引发异常。
'''

def do_count(table_name, milvus_cli):
    if not table_name:
        table_name = DEFAULT_TABLE
    try:
        if not milvus_cli.has_collection(table_name):
            return None
        num = milvus_cli.count(table_name)
        return num
    except Exception as e:
        LOGGER.error(f"Error with count table {e}")
        # sys.exit(1)
        raise e