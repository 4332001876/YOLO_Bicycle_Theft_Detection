import pickle
import base64
from server.config import DEFAULT_TABLE


def do_update(uploadImagesModel, img_path, model, milvus_client, mysql_cli):
    table_name = uploadImagesModel.table
    if not table_name:
        table_name = DEFAULT_TABLE
    # 删除原有milvus 数据
    ms_data = mysql_cli.search_by_ids( [uploadImagesModel.id],table_name)
    if len(ms_data) == 0:
        raise Exception("id not exist")
    milvus_client.delete(table_name, "id in [%s]" % ms_data[0][1])

    feat = model.resnet50_extract_feat(img_path)
    ids = milvus_client.insert(table_name, [feat])
    # milvus_client.create_index(table_name)

    try:
        # mysql_cli.create_mysql_table(table_name)
        return mysql_cli.update(table_name, (ids[0], uploadImagesModel.tags, uploadImagesModel.brief,base64.b64encode(pickle.dumps(feat)).decode(),uploadImagesModel.id))
    except Exception as e:
        milvus_client.delete(table_name, "id in [%s]" % ids[0])
        raise e
    
'''
首先，函数从uploadImagesModel中获取表名，并将其存储在table_name变量中。如果表名为空，则使用名为DEFAULT_TABLE的默认表。

接下来，函数调用mysql_cli的search_by_ids方法，根据给定的ID从MySQL数据库中检索数据，并将结果存储在ms_data变量中。

如果ms_data的长度为0，即没有找到与给定ID相对应的数据，则抛出一个异常。

否则，函数调用milvus_client的delete方法，根据MySQL数据库中检索到的ID，在Milvus中删除相应的向量。

然后，函数调用model的resnet50_extract_feat方法，对给定的图像路径img_path进行特征提取，并将结果存储在feat变量中。

接着，函数调用milvus_client的insert方法，将提取得到的特征feat插入到指定的表table_name中，返回插入的向量ID，并将结果存储在ids变量中。

尝试执行以下操作：

调用mysql_cli的update方法，将更新的信息作为参数传递，更新MySQL数据库中与ID对应的记录。更新的信息包括新的向量ID、标签、简介和经过pickle模块序列化后使用base64编码的特征。
如果更新操作成功，则返回结果。
如果在执行更新操作时出现异常，函数捕获该异常，并先调用milvus_client的delete方法，根据Milvus向量的ID删除已插入的向量，然后抛出原始异常。

总体而言，do_update函数的功能是在Milvus和MySQL数据库中更新指定ID对应的记录。它先根据ID从MySQL数据库检索原始数据，并在Milvus中删除相应的向量。然后，它使用给定的图像路径提取特征，并将特征插入到Milvus中，并更新MySQL数据库中与ID对应的记录。最后，它返回更新结果。
'''