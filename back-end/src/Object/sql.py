import pymysql
import os

db_host = os.getenv('DB_HOST', '')
db_user = os.getenv('DB_USER', '')
db_pass = os.getenv('DB_PASS', '')
db_name = os.getenv('DB_NAME', '')


class sql:

    def get(query, data):
        db = pymysql.connect(db_host,db_user,db_pass,db_name)
        cursor = db.cursor()
        cursor.execute(query, data)
        to_ret =  cursor.fetchall()
        cursor.close()
        db.close()
        return to_ret

    def input(query, data):
        db = pymysql.connect(db_host,db_user,db_pass,db_name)
        cursor = db.cursor()
        try:
            cursor.execute(query, data)
            db.commit()
            to_ret = True
        except:
            db.rollback()
            to_ret = False
        cursor.close()
        db.close()
        return to_ret
