import pickle
import base64
from server.config import DEFAULT_TABLE


def do_upload(uploadImagesModel, img_path, model, milvus_client, mysql_cli):
    """
    解析图片特征并入口
    :param uploadImagesModel:
    :param img_path:
    :param model:
    :param milvus_client:
    :param mysql_cli:
    :return:
    """
    table_name = uploadImagesModel.table
    if not table_name:
        table_name = DEFAULT_TABLE
    feat = model.resnet50_extract_feat(img_path)
    ids = milvus_client.insert(table_name, [feat])
    # milvus_client.create_index(table_name)
    try:
        # mysql_cli.create_mysql_table(table_name)
        return mysql_cli.insert(table_name, (ids[0],uploadImagesModel.tags, uploadImagesModel.brief,base64.b64encode(pickle.dumps(feat)).decode()))
    except Exception as e:
        raise e
'''
首先，函数从uploadImagesModel中获取表名，并将其存储在table_name变量中。如果表名为空，则使用名为DEFAULT_TABLE的默认表。

接下来，函数调用model的resnet50_extract_feat方法，对给定的图像路径img_path进行特征提取，并将结果存储在feat变量中。

然后，函数调用milvus_client的insert方法，将提取得到的特征feat插入到指定的表table_name中，返回插入的向量ID，并将结果存储在ids变量中。

尝试执行以下操作：

调用mysql_cli的insert方法，将插入的信息作为参数传递，将新记录插入到MySQL数据库中。插入的信息包括新的向量ID、标签、简介和经过pickle模块序列化后使用base64编码的特征。
如果插入操作成功，则返回结果。
如果在执行插入操作时出现异常，函数捕获该异常，并抛出原始异常。

总体而言，do_upload函数的功能是将给定图像路径的特征提取并插入到Milvus和MySQL数据库中。它首先将表名从uploadImagesModel中获取或使用默认表名。然后，它使用给定的图像路径提取特征，并将特征插入到Milvus中，并插入新记录到MySQL数据库中。最后，它返回插入结果。
'''