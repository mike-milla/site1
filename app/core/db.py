import json
import pymysql
import pymysql.cursors


class Connection:
    def __init__(self):
        self.conn = pymysql.connect(host="localhost",
                                    user="root",
                                    password="",
                                    database="tt")

    def Write(self, query, data):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, data)
                self.conn.commit()
                return True
        except Exception as e:
            print(f"ERROR: {e}")
            self.conn.rollback()
            return

    def Read(self, query, *data):
        data = tuple(data)
        if len(data):
            if type(data[0]) == list:
                data = data[0]
        try:
            self.conn.ping()
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                if data:
                    cursor.execute(query, data)
                else:
                    cursor.execute(query)
                if cursor.rowcount == 0:
                    result = False
                elif cursor.rowcount == 1:
                    result = cursor.fetchone()
                    cursor.close()
                else:
                    result = cursor.fetchall()
                    cursor.close()

            return result
        finally:
            print("dfgeger")


class Database:
    conn = None
    returnType = "all"
    @classmethod
    def __init(cls):
        cls.conn = pymysql.connect(host="localhost",
                                   user="root",
                                   password="",
                                   database="tt")

    @classmethod
    def return_ll(cls):
        cls.returnType = "all"
        return cls

    @classmethod
    def write(cls, query, data):
        try:
            with cls.conn.cursor() as cursor:
                cursor.execute(query, data)
                cls.conn.commit()
                return True
        except Exception as e:
            print(f"ERROR: {e}")
            cls.conn.rollback()
            return

    @classmethod
    def read(cls, query, *data):
        data = tuple(data)
        if len(data):
            if type(data[0]) == list:
                data = data[0]
        try:
            cls.__init()
            cls.conn.ping()
            with cls.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                if data:
                    cursor.execute(query, data)
                else:
                    cursor.execute(query)
                if cursor.rowcount == 0:
                    result = False

                elif cls.returnType == "all":
                    result = cursor.fetchall()
                    cursor.close()

                elif cursor.rowcount == 1:
                    result = cursor.fetchone()
                    cursor.close()
                else:
                    result = cursor.fetchall()
                    cursor.close()

            return result
        except Exception as e:
            print()


DB = Connection()
