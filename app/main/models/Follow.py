from . import *
from . import Main
from .. import make_res
from ...core.db import Connection,Database


class Follow(Main):
    @classmethod
    def followers(cls, d):
        sql = f"SELECT * from {cls.T_USERS} where uid != %s and uid in (select followerid from {cls.T_FOLLOW} where followingid = %s) order by rand() limit %s,%s "
        filters = d.get('filters')
        lm = d.get('limits')
        uid = d.get('uid')
        if lm:
            l = lm['from']
            r = lm['to']
        else:
            l = 0
            r = 10
        vals = [uid, uid, l, r]
        return Connection().Read(sql, vals)

    @classmethod
    def count_followers(cls,uid):
        sql = f"SELECT COUNT(followingid) as count FROM {cls.T_FOLLOW} WHERE followingid = %s"
        d = Connection().Read(sql, uid)
        if d  and d.get("count"):
            return int(d.get("count"))
        return


    @classmethod
    def count(cls):
        j = request.json
        print(j)
        data = j.get("data")
        if not data:
            return make_res(msg="null_request")
        uid = data.get("uid")
        if not uid:
            return make_res(msg="cannot read data for null target")
        sql = f"SELECT COUNT(followingid) as count FROM {cls.T_FOLLOW} WHERE followingid = %s"
        d = Connection().Read(sql, uid)
        return make_res(msg="success" if d else "error requesting", res=d if d else '')

    @classmethod
    def i_follow(cls, uid, you):
        sql = f"SELECT followerid , followingid FROM {cls.T_FOLLOW} WHERE followerid =%s and followingid = %s"
        sql = Connection().Read(sql, [uid, you])
        return True if sql else False

    @classmethod
    def fcount(cls, following=0):
        j = request.json
        data = j.get("data")
        if not data:
            return make_res(msg="null_request")
        uid = data.get("uid")
        if not uid:
            return make_res(msg="cannot read data for null target")
        sql = f"SELECT COUNT(followingid) as count FROM {cls.T_FOLLOW} WHERE followingid = %s"
        if following == 1:
            sql = f"SELECT COUNT(followerid) as count FROM {cls.T_FOLLOW} WHERE followerid = %s"
        d = Connection().Read(sql, uid)
        return make_res(success=1 if d else 0, msg="success" if d else "error requesting", res=d if d else '')


class Following(Follow):
    @classmethod
    def count(cls):
        return cls.fcount(following=1)
    @classmethod
    def info(cls):
        j = request.json
        data = j.get("data")
        if not data:
            return cls.data_error()
        uid = data.get("uid")
        if not uid:
            return cls.value_error()
        sql = f"SELECT * from {cls.T_USERS} where uid != %s and uid in (select followingid from {cls.T_FOLLOW} where followerid = %s)"
        d = Database.return_ll().read(sql, uid,uid)
        return make_res(success=1 , res=d)


    @classmethod
    def check(cls):
        j = request.json.get("data")

        if not j:
            return make_res(msg="no data found")

        me = j.get("me")
        you = j.get("you")
        ifl = cls.i_follow(me, you)
        if ifl:
            return make_res(res=ifl,success=1)

        return make_res(msg="something went wrong")

    @classmethod
    def add(cls):
        j = request.json.get("data")

        if not j:
            return make_res(msg="no data found")

        me = j.get("me")
        you = j.get("you")

        data = {
            'followerid': me,
            'followingid': you,
            'time': getNow(),
        }
        if cls.i_follow(me, you):
            return make_res(msg="something went wrong")

        if cls.create(cls.T_FOLLOW, data):
            data_notify = {
                'for_': you,
                'from_': me,
                'target': 0,
                'type': 'follow',
                'time': getNow(),
                'count': '0',
                'status': '0'
            }
            if cls.create(cls.T_NOTE, data_notify):
                return make_res(msg="success", success=1)
        return make_res(msg="something went wrong")


class Follower(Follow):
    @classmethod
    def count(cls):
        return cls.fcount()

    


    
