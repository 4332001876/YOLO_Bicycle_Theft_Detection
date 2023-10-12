import pymysql
from server.config import *
from server.logs import LOGGER


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
        sql = "CREATE TABLE IF NOT EXISTS "+table_name+"  ( id INT ( 10 ) UNSIGNED NOT NULL AUTO_INCREMENT,milvus_id INT ( 10 ), bicycle_id INT( 10 ), location_description varchar(200), feature MEDIUMTEXT,upload_status tinyint(2) DEFAULT '0', create_date datetime ( 3 ) DEFAULT CURRENT_TIMESTAMP ( 3 ), modify_date datetime ( 3 ) DEFAULT CURRENT_TIMESTAMP ( 3 ) ON UPDATE CURRENT_TIMESTAMP ( 3 ), PRIMARY KEY ( `id` ), KEY `index_bicycle_id` ( `bicycle_id` ) USING BTREE, KEY `index_milvus_id` ( `milvus_id` )  ) ENGINE = INNODB DEFAULT CHARSET = utf8;"

        self.cursor.execute(sql)

    def load_data_to_mysql(self, table_name, data):
        # 批量插入数据
        self.test_connection()
        sql = "insert into " + table_name + \
            " (milvus_id,bicycle_id,location_description) values (%s,%s,%s);"

        self.cursor.executemany(sql, data)
        self.cursor.insert_id()
        self.conn.commit()

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

    def update(self, table_name, data):
        self.test_connection()
        sql = "update " + table_name + \
            " set milvus_id = %s,bicycle_id = '%s', location_description='%s',feature = '%s' where id = %s;" % data
        n = self.cursor.execute(sql)
        self.conn.commit()
        return n

    def update_status(self, table_name, data):
        # 更新upstatus状态
        self.test_connection()
        sql = "update " + table_name + \
            " set milvus_id = %s,upload_status= %s  where id = %s;" % data
        n = self.cursor.execute(sql)
        self.conn.commit()
        return n

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

    def search_by_update_status(self, table_name, upload_status, limit):
        self.test_connection()
        sql = "select id,milvus_id,bicycle_id,location_decription,feature from %s where upload_status = %s limit %s ;" % (table_name, upload_status, limit)
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return results


    def delete_by_id(self, table_name, id):
        self.test_connection()
        sql = "delete from %s where id = %s" % (table_name, id)
        self.cursor.execute(sql)
        self.conn.commit()
        LOGGER.debug(f"MYSQL delete {id} data in table:{table_name}")

    def count_table(self, table_name):
        # Get the number of mysql table
        self.test_connection()
        sql = "select count(milvus_id) from " + table_name + ";"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
