import pymysql
from server.config import *
from datetime import datetime, timedelta
from reid_pipeline.reid_data_manager import DetectedObject

class MySQLHelper:
    def __init__(self):
        self.conn = pymysql.connect(host=MYSQL_HOST,
                                    user=MYSQL_USER,
                                    port=MYSQL_PORT,
                                    password=MYSQL_PWD,
                                    database=None,
                                    local_infile=True)
        
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS "+MYSQL_DB+" DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;")
        self.cursor.execute("USE "+MYSQL_DB+";")

    def test_connection(self):
        try:
            self.conn.ping()
        except Exception:
            self.conn = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, port=MYSQL_PORT, password=MYSQL_PWD,
                                        database=MYSQL_DB, local_infile=True)
            self.cursor = self.conn.cursor()

    def create_mysql_table(self, table_name):
        # Create mysql table if not exists
        self.test_connection()
        sql = "CREATE TABLE IF NOT EXISTS "+table_name
        + " (id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT, bicycle_id BIGINT UNSIGNED DEFAULT NULL, camera_id INT UNSIGNED DEFAULT NULL, feature TEXT DEFAULT NULL, start_time datetime DEFAULT NULL,end_time datetime(30) DEFAULT NULL,"
        + "create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP PRIMARY KEY ( `id` ), KEY `index_bicycle_id` ( `bicycle_id` ) USING BTREE ) ENGINE = INNODB DEFAULT CHARSET = utf8;"

        self.cursor.execute(sql)

    def insert(self, table_name, bike_id, obj: DetectedObject):
        # 单条数据插入，返回最后一行id
        self.test_connection()
        time_str = "%s"%datetime.fromtimestamp(obj.time)
        sql = "insert into " + table_name + \
            " (bicycle_id,camera_id,feature,start_time,end_time) values ('%d','%d','','%f','%f');" % (bike_id, obj.cam_id, time_str, time_str)
        n = self.cursor.execute(sql)
        if n > 0:
            ms_id = self.cursor.lastrowid
            self.conn.commit()
        else:
            self.conn.rollback()
        return ms_id


    def search_by_bicycle_id(self, bike_id, table_name):
        self.test_connection()
        sql = "select id,bicycle_id,camera_id,feature,start_time,end_time from " + \
            table_name + " where bicycle_id in '%s' ;" % bike_id
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return results

    def search_by_ids(self, ids, table_name):
        self.test_connection()
        str_ids = str(ids).replace('[', '').replace(']', '')
        sql = "select id,bicycle_id,camera_id,feature,start_time,end_time from " + \
            table_name + " where id in (" + str_ids + ");"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return results


    def delete_by_id(self, table_name, id):
        self.test_connection()
        sql = "delete from %s where id = %s" % (table_name, id)
        self.cursor.execute(sql)
        self.conn.commit()


    def update(self, table_name, data):
        # Batch insert (Milvus_ids, img_path) to mysql
        self.test_connection()
        sql = "update " + table_name + " set bicycle_id = %s,camera_id = '%s', feature='%s',start_time='%s',edn_time='%s'" % data
        n = self.cursor.execute(sql)
        self.conn.commit()


    def auto_delete_TimeExpired(self,table_name):
        self.test_connection()
        # 计算7天前的时间
        time_limit = datetime.now() - timedelta(days=MYSQL_DELETE_INTERVAL)
        sql = f"DELETE FROM" + table_name+"WHERE create_time < '{time_limit}'"
        self.cursor.execute(sql)
        self.conn.commit()        
        rows_deleted = self.cursor.rowcount
        self.cursor.close()
        return rows_deleted#返回受影响的列

