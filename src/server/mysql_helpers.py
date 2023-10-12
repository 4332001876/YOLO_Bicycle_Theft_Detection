import pymysql
from server.config import *


class MySQLHelper():

    def __init__(self):
        self.conn = pymysql.connect(host=MYSQL_HOST,
                                    user=MYSQL_USER,
                                    port=MYSQL_PORT,
                                    password=MYSQL_PWD,
                                    database=MYSQL_DB,
                                    local_infile=True)
        self.cursor = self.conn.cursor()

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
        sql = "CREATE TABLE IF NOT EXISTS "+table_name+"  ( id INT ( 10 ) UNSIGNED NOT NULL AUTO_INCREMENT, bicycle_id INT( 10 ) DEFAULT NULL, camera_id varchar(20) DEFAULT NULL, feature MEDIUMTEXT DEFAULT NULL,, start_time varchar(30) DEFAULT NULL,end_time varchar(30) DEFAULT NULL, PRIMARY KEY ( `id` ), KEY `index_bicycle_id` ( `bicycle_id` ) USING BTREE ) ENGINE = INNODB DEFAULT CHARSET = utf8;"

        self.cursor.execute(sql)

    def insert(self, table_name, data):
        # 单条数据插入，返回最后一行id
        self.test_connection()
        
        sql = "insert into " + table_name + \
            " (milvus_id,bicycle_id,location_description,upload_status) values ('%s','%s','%s','%s',1);" % data
        n = self.cursor.execute(sql)
        if n > 0:
            ms_id = self.cursor.lastrowid
            self.conn.commit()
        else:
            self.conn.rollback()
        return ms_id


    def search_by_milvus_ids(self, ids, table_name):
        self.test_connection()
        str_ids = str(ids).replace('[', '').replace(']', '')
        sql = "select id,milvus_id,bicycle_id,location_decription from " + \
            table_name + " where milvus_id in (" + str_ids + ");"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return results

    def search_by_ids(self, ids, table_name):
        self.test_connection()
        str_ids = str(ids).replace('[', '').replace(']', '')
        sql = "select id,milvus_id,bicycle_id,location_decription from " + \
            table_name + " where id in (" + str_ids + ");"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return results


    def delete_by_id(self, table_name, id):
        self.test_connection()
        sql = "delete from %s where id = %s" % (table_name, id)
        self.cursor.execute(sql)
        self.conn.commit()

    def count_table(self, table_name):
        # Get the number of mysql table
        self.test_connection()
        sql = "select count(milvus_id) from " + table_name + ";"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
