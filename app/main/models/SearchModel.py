from . import *
from .. import make_res
from ...core.db import Database


class Search(Main):
    @classmethod
    def get_user_search(cls, text):
        d = cls.__data(cls.T_USERS, uname=text, fname=text, lname=text, field=text)
        return make_res(success=1, res=d)

    @classmethod
    def get_feed_search(cls, text):
        d = cls.__data(cls.T_FEEDS, status=text)
        return make_res(success=1, res=d)

    @classmethod
    def __data(cls, table, **keys):
        keys = dict(keys)
        if not len(keys):
            return
        sql = f"SELECT * FROM {table} where "
        vals = []
        for key, val in keys.items():
            sql += f" {keys} like %s OR "
            vals.append(f"%{val}%")

        sql = sql.rstrip(" OR ")

        return Database.read(sql, vals)
