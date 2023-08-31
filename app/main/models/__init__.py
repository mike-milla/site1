from .. import *
from flask_jwt_extended import create_access_token, jwt_required, create_refresh_token


class Main:
    THEME_1 = "light"
    THEME_2 = "dark"
    THEME_3 = "lightsout"
    # Define constants for fonts
    FONT_1 = "smaller"
    FONT_2 = "small"
    FONT_3 = "normal"
    FONT_4 = "large"
    FONT_5 = "larger"
    # Define constants for SQL tables
    T_POSTS = "app_posts"
    T_FEEDS = "app_feeds"
    T_NOTES = "app_note"
    T_LIKES = "app_likes"
    T_COMMENT = "app_comment"
    T_COLLECTIONS = "app_collections"
    T_MESSAGES = "app__msg"
    T_USERS = 'app_users'
    T_FOLLOW = 'app_follow'
    T_NOTE = "app_note"
    T_SAVE = "app_usersave"
    T_USER_CONFIG = 'app_user_config'
    T_RATING = "app_ratings"


    def __init__(self):
        pass

    @classmethod
    def create(cls, table, fields=None):
        if fields is None:
            fields = {}
        cols = ', '.join(fields.keys())
        vals = []
        v1 = ''
        for key, value in fields.items():
            v1 += ' %s, '
            vals.append(value)
        v1 = v1.rstrip(', ')
        sql = f"INSERT INTO {table} ({cols}) VALUES ({v1})"
        if Connection().Write(sql, vals):
            return True
        return

    @classmethod
    def delete(cls, table, **condition):
        sql = f"DELETE FROM {table} WHERE "
        vals = []
        for key, value in condition.items():
            sql += f"{key} = %s AND "
            vals.append(value)
        sql = sql.rstrip(" AND ")
        if Connection().Write(sql, vals):
            return True
        return

    @classmethod
    def update(cls, table, uid, fields=None, keyw='uid'):
        if fields is None:
            fields = {}
        cols = ''
        loopCount = 1
        vals = []
        for name, value in fields.items():
            cols += f"`{name}` = %s "
            vals.append(value)
            if loopCount < len(fields):
                cols += ', '
            loopCount += 1

        sql = f"UPDATE {table} SET {cols} WHERE {keyw} = %s"
        vals.append(uid)
        if DB.Write(sql, vals):
            return True
        return

    @classmethod
    def t_update(cls, table, fields=None, **conditions):
        if fields is None:
            fields = {}
        cols = ''
        loopCount = 1
        vals = []
        for name, value in fields.items():
            cols += f"`{name}` = %s "
            vals.append(value)
            if loopCount < len(fields):
                cols += ', '
            loopCount += 1

        sql = f"UPDATE {table} SET {cols} WHERE "

        for key in conditions:
            sql += f" {key} = %s AND"
            vals.append(conditions[key])
        sql = sql.rstrip(" AND ")
        if DB.Write(sql, vals):
            return True
        return

    @classmethod
    def t_data_and(cls,table,**fields):
        fields = dict(fields)
        vals = []
        sql = f"select * from {table} where "
        for name, value in fields.items():
            sql += f" {name} = %s and "
            vals.append(value)

        sql = sql.rstrip(" and ")
        return Connection().Read(sql, vals)

    @classmethod
    def t_data_or(cls, table, **fields):
        fields = dict(fields)
        vals = []
        sql = f"select * from {table} where "
        for name, value in fields.items():
            sql += f" {name} = %s or "
            vals.append(value)

        sql = sql.rstrip(" or ")
        return Connection().Read(sql, vals)

    @staticmethod
    def data_error():
        return make_res(msg="Data Error: no data passed")

    @staticmethod
    def value_error():
        return make_res(msg="Value Error: all values are required")

    @staticmethod
    def unknown_error():
        return make_res(msg="Unkown error occured")


from .Config import *
from .User import *
from .Follow import *
from .Feeds import *
from .Likes import *
from .Messages import *
from .AuthModel import *

from .Collection import *
from .Star import *

from .SearchModel import *
