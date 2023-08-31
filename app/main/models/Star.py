from . import *
from .. import make_res, gen_random
from ...core.db import Database


class Star(Main):
    @classmethod
    def __data(cls, **data):
        try:
            data = dict(data)
            if not len(data):
                return
            sql = f"select * from {cls.T_RATING} where "
            val = []
            for key in data:
                sql += f" {key}=%s AND "
                val.append(data[key])
            sql = sql.rstrip(" AND ")
            return Connection().Read(sql, val)
        except Exception as e:
            return

    @classmethod
    def count_user_stars(cls):
        d = request.json.get("data").get("uid") or None
        if not d:
            return cls.data_error()

        sql = f"SELECT rating FROM {cls.T_RATING} WHERE target = %s"
        sql = Database.return_ll().read(sql, d)
        ratings = 0
        if sql:
            for rt in sql:

                ratings += float(rt.get("rating"))

        print(ratings)
        return make_res(success=1, res={"count": ratings})

    @classmethod
    def count_feed_stars(cls):
        d = request.json.get("data").get("post_id") or None
        if not d:
            return cls.data_error()

        sql = f"SELECT rating FROM {cls.T_RATING} WHERE post_id = %s"
        sql = Database.return_ll().read(sql, d)
        ratings = 0
        if sql:
            for rt in sql:
                ratings += float(rt.get("rating"))

        print(ratings)
        return make_res(success=1, res={"count": ratings})

    @classmethod
    def add(cls):
        data = request.json.get("data")
        if not data:
            return make_res(msg="application Error: no data")

        data = sanitize_data(data)

        t = data.get("target")
        uid = data.get("user_id")
        p_id = data.get("post_id")
        rating = data.get("rating")

        if not t or not uid or not p_id or not rating:
            return make_res(msg="application Error: all params required")

        uf = Follow.count_followers(uid)

        if not can_rate(rating, uf):
            return make_res(msg="Try a lower rating")

        if cls.__data(uid=uid, post_id=p_id, target=t):
            if float(rating) <= 0:
                return make_res(msg="Once stared, you can't add null stars")
            if cls.t_update(cls.T_RATING, {"rating": rating}, uid=uid, post_id=p_id, target=t):
                return make_res(success=1)
            return make_res(msg="application Error")

        data = {
            "rate_id": gen_random(20),
            "rating": rating,
            "post_id": p_id,
            "target": t,
            "uid": uid,
            "date": getNow()
        }
        if cls.create(cls.T_RATING, data):
            data_notify = {'for_': t,
                           'from_': uid,
                           'target': p_id,
                           'type': 'star',
                           'time': getNow(),
                           'count': '0',
                           'status': '0'
                           }
            cls.create(cls.T_NOTE, data_notify)
            return make_res(success=1)
