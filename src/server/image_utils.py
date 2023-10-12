import base64
import pickle


'''
    对象转 str.先使用 pickle.dumps 方法将对象进行序列化，然后使用 base64.b64encode 方法对序列化后的字节串进行 Base64 编码，最后通过 decode 方法将字节串转换为字符串并返回。
'''
def obj_encode(obj):
    return base64.b64encode(pickle.dumps(obj)).decode()



'''
    str 转对象
'''
def obj_decode(objStr):
    return pickle.loads(base64.b64decode(objStr))

