from ..server.config import DEFAULT_TABLE


def do_search(table_name, img_path, top_k, model, milvus_client, mysql_cli):
    if not table_name:
        table_name = DEFAULT_TABLE
    feat = model.resnet50_extract_feat(img_path)
    vectors = milvus_client.search_vectors(table_name, [feat], top_k)
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
        data['tags'] = paths[i][2]
        data['brief'] = paths[i][3]
        data['distance'] = vectors_dict.get(int(paths[i][1]))
        res.append(data)
    return res

'''
首先，函数会检查table_name的值是否为空，如果为空，则使用名为DEFAULT_TABLE的默认表。

接下来，函数调用model的resnet50_extract_feat方法，对给定的图像路径img_path进行特征提取，并将结果存储在feat变量中。

然后，函数通过调用milvus_client的search_vectors方法，在指定的表table_name中搜索与提取得到的特征最相似的前top_k个向量。搜索结果存储在vectors变量中。

接着，函数初始化一个空列表res，用于存储最终的搜索结果。

如果vectors[0]的长度为0，即没有找到与提取特征相似的向量，函数直接返回一个空列表。

否则，函数迭代遍历vectors[0]中的每个向量，将其ID作为键、距离作为值，构建一个字典vectors_dict。

接着，函数调用mysql_cli的search_by_milvus_ids方法，根据Milvus向量的ID从MySQL数据库中检索信息，并将结果存储在paths变量中。

然后，函数使用paths的长度作为迭代的次数，遍历每个结果，构建一个字典data，包含ID、标签、简介和距离信息。然后将字典data添加到结果列表res中。

最后，函数返回结果列表res，其中每个元素都是一个包含搜索结果的字典。

总体而言，do_search函数的功能是在Milvus中根据提取的特征搜索相似向量，并根据Milvus向量的ID从MySQL数据库中提取与之相关的信息，返回包含搜索结果的列表。

'''