from . import *
from . import Main
from .. import make_res


class Collection(Main):
    @classmethod
    def for_user(cls, user):
        sql = f"SELECT * from {cls.T_COLLECTIONS} where uid = %s"
        d = Connection().Read(sql, user)
        return make_res(success=1,res=d)

    @classmethod
    def add_to_collection(cls):
        d = request.json.get("data")
        if not d:
            return make_res(msg=f"application Error:No data")

        d = sanitize_data(d)
        d["date"] = getNow()
        if cls.__data(d.get("postid"),d.get("uid")):
            return make_res(msg="application Error:Already saved")
        if cls.create(cls.T_SAVE, d):
            return make_res(success=1)
        return make_res(msg="application Error")

    @classmethod
    def create_collection(cls):
        pass



    @classmethod
    def is_saved(cls,postid,userid):
        return cls.__data()

    @classmethod
    def __data(cls,postid,userid):
        sql = f"select * from {cls.T_SAVE} where uid=%s and postid = %s"
        return Connection().Read(sql,[userid,postid])

