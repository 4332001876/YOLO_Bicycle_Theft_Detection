import pymysql
from config import *
from logs import LOGGER


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
        sql = "CREATE TABLE IF NOT EXISTS "+table_name+"  ( id BIGINT ( 20 ) UNSIGNED NOT NULL AUTO_INCREMENT, milvus_id BIGINT ( 20 ), tags VARCHAR ( 32 ), brief VARCHAR ( 500 ), feature MEDIUMTEXT, upload_status tinyint(2) DEFAULT '0', create_date datetime ( 3 ) DEFAULT CURRENT_TIMESTAMP ( 3 ), modify_date datetime ( 3 ) DEFAULT CURRENT_TIMESTAMP ( 3 ) ON UPDATE CURRENT_TIMESTAMP ( 3 ), PRIMARY KEY ( `id` ), KEY `idx_tags` ( `tags` ) USING BTREE, KEY `idx_milvus_id` ( `milvus_id` )  ) ENGINE = INNODB DEFAULT CHARSET = utf8;"
        
        
        '''
        这是在MySQL数据库中创建表的SQL语句。此表包含以下列：

        id：自增主键。
        milvus_id：用于与Milvus向量库中的向量进行匹配的id。
        tags：用于存储图片标签的字符串。
        brief：用于存储图片简介的字符串。
        feature：用于存储图片特征向量的文本格式字符串。
        upload_status：用于表示此条数据是否已经上传到Milvus向量库中。
        create_date：用于记录此数据的创建时间。
        modify_date：用于记录此数据的修改时间。
        PRIMARY KEY：将id列设置为主键。
        KEY idx_tags：对tags列创建索引，用于提高查询效率。
        KEY idx_milvus_id：对milvus_id列创建索引，用于提高匹配效率。
        ENGINE = INNODB：指定使用InnoDB存储引擎。
        DEFAULT CHARSET = utf8：指定表的字符集为utf8。
        通过执行此SQL语句，可以创建一个名为table_name的表（如果此表不存在）并定义它的各种列及其他属性。
        '''
        
        self.cursor.execute(sql)
        LOGGER.debug(f"MYSQL create table: {table_name} with sql: {sql}")

    def load_data_to_mysql(self, table_name, data):
        # Batch insert (Milvus_ids, img_path) to mysql
        self.test_connection()
        sql = "insert into " + table_name + " (milvus_id,tags,brief) values (%s,%s,%s);"
        try:
            self.cursor.executemany(sql, data)
            self.cursor.insert_id()
            self.conn.commit()
            LOGGER.debug(f"MYSQL loads data to table: {table_name} successfully")
        except Exception as e:
            LOGGER.error(f"MYSQL ERROR: {e} with sql: {sql}")
            # sys.exit(1)
            raise e

    def insert(self, table_name, data):
        # Batch insert (Milvus_ids, img_path) to mysql
        self.test_connection()
        sql = "insert into " + table_name + " (milvus_id,tags,brief,feature,upload_status) values ('%s','%s','%s','%s',1);" % data
        n = self.cursor.execute(sql)
        if n > 0:
            ms_id = self.cursor.lastrowid
            self.conn.commit()
        else:
            self.conn.rollback()
            raise Exception("ms insert fail")
        LOGGER.debug(f"MYSQL loads data to table: {table_name} successfully")
        return ms_id

    def update(self, table_name, data):
        # Batch insert (Milvus_ids, img_path) to mysql
        self.test_connection()
        sql = "update " + table_name + " set milvus_id = %s,tags = '%s', brief='%s',feature='%s' where id = %s;" % data
        n = self.cursor.execute(sql)
        self.conn.commit()
        LOGGER.debug(f"MYSQL loads data to table: {table_name} successfully")
        return n

    def update_status(self, table_name, data):
        # Batch insert (Milvus_ids, img_path) to mysql
        self.test_connection()
        sql = "update " + table_name + " set milvus_id = %s,upload_status= %s  where id = %s" % data
        n = self.cursor.execute(sql)
        self.conn.commit()
        LOGGER.debug(f"MYSQL loads data to table: {table_name} successfully")
        return n

    def search_by_milvus_ids(self, ids, table_name):
        # Get the img_path according to the milvus ids
        self.test_connection()
        str_ids = str(ids).replace('[', '').replace(']', '')
        sql = "select id,milvus_id,tags,brief from " + table_name + " where milvus_id in (" + str_ids + ");"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        LOGGER.debug("MYSQL search by milvus id.")
        return results

    def search_by_ids(self, ids, table_name):
        # Get the img_path according to the milvus ids
        self.test_connection()
        str_ids = str(ids).replace('[', '').replace(']', '')
        sql = "select id,milvus_id,tags,brief from " + table_name + " where id in (" + str_ids + ");"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        LOGGER.debug("MYSQL search by milvus id.")
        return results

    def search_by_update_status(self, table_name, upload_status, limit):
        # Get the img_path according to the milvus ids
        self.test_connection()
        sql = "select id,milvus_id,tags,brief,feature from %s where upload_status = %s limit %s " % (
        table_name, upload_status, limit)
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        LOGGER.debug("MYSQL search by milvus id.")
        return results

    def delete_table(self, table_name):
        # Delete mysql table if exists
        self.test_connection()
        sql = "drop table if exists " + table_name + ";"
        try:
            self.cursor.execute(sql)
            LOGGER.debug(f"MYSQL delete table:{table_name}")
        except Exception as e:
            LOGGER.error(f"MYSQL ERROR: {e} with sql: {sql}")
            # sys.exit(1)
            raise e
    def delete_all_data(self, table_name):
        # Delete all the data in mysql table
        self.test_connection()
        sql = 'TRUNCATE table ' + table_name + ';'
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            LOGGER.debug(f"MYSQL delete all data in table:{table_name}")
        except Exception as e:
            LOGGER.error(f"MYSQL ERROR: {e} with sql: {sql}")
            # sys.exit(1)
            raise e

    def delete_by_id(self, table_name, id):
        # Delete all the data in mysql table
        self.test_connection()
        sql = "delete from %s where id = %s" % (table_name, id)
        self.cursor.execute(sql)
        self.conn.commit()
        LOGGER.debug(f"MYSQL delete {id} data in table:{table_name}")

    def count_table(self, table_name):
        # Get the number of mysql table
        self.test_connection()
        sql = "select count(milvus_id) from " + table_name + ";"
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            LOGGER.debug(f"MYSQL count table:{table_name}")
            return results[0][0]
        except Exception as e:
            LOGGER.error(f"MYSQL ERROR: {e} with sql: {sql}")
            # sys.exit(1)
            raise e