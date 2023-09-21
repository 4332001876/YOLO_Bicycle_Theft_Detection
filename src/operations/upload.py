import sys
import pickle
import base64
sys.path.append("..")
from config import DEFAULT_TABLE


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