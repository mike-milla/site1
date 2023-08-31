from . import *
class Config(Main):
    @classmethod
    def set_theme(cls,uid, theme_id, n=False):
        themes = {
            1: cls.THEME_1,
            2: cls.THEME_2,
            3: cls.THEME_3
        }

        if n:
            data = {
                "theme": themes[theme_id],
                "uid": uid,
            }
            cls.create(cls.T_USER_CONFIG, data)
        else:
            data = {
                "theme": themes[theme_id],
            }
            cls.update(cls.T_USER_CONFIG, uid, data)

    @classmethod
    def get_theme(cls,uid):
        q = DB.Read(f"SELECT * from {cls.T_USER_CONFIG} where uid = %s",uid)
        return q