from . import *


class Like(Main):
    @classmethod
    def count(cls, p_id):
        p_id = sanitize_input(p_id)
        sql = f"SELECT COUNT(post_id) as count FROM {cls.T_LIKES} WHERE post_id =%s "
        s = Connection().Read(sql, p_id)
        return make_res(res=s or None, success=1 if s else 0)

    @classmethod
    def add_like(cls):
        data = request.json.get("data") or None
        if not data:
            return cls.data_error()

        data = sanitize_data(data)
        p_id = data.get("post_id")
        uid = data.get("uid")
        target = data.get("target")

        if not p_id or not uid or not target:
            return cls.value_error()

        data_notify = {
            'for_': target,
            'from_': uid,
            'target': p_id,
            'type': 'like',
            'time': getNow(),
            'count': '0',
            'status': '0'
        }

        if cls.create(cls.T_LIKES, {"uid": uid, "post_id": p_id}):
            if uid != target:
                cls.create(cls.T_NOTE, data_notify)
            return make_res(success=1)
        return cls.unknown_error()

    @classmethod
    def remove_like(cls):
        data = request.json.get("data") or None
        if not data:
            return cls.data_error()

        data = sanitize_data(data)
        p_id = data.get("post_id")
        uid = data.get("uid")
        target = data.get("target")

        if not p_id or not uid or not target:
            return cls.value_error()

        if cls.delete(cls.T_LIKES, uid=uid, post_id= p_id):
            cls.delete(cls.T_NOTE, target=p_id, for_=target,from_=uid,type="like")
            return make_res(success=1)
        return cls.unknown_error()


    @classmethod
    def i_like(cls):
        data = request.json.get("data") or None
        if not data:
            return cls.data_error()

        uid = data.get("uid")
        post_id = data.get("post_id")
        target = data.get("target")
        if cls.t_data_and(cls.T_LIKES,uid=uid,post_id=post_id):
            return make_res(res=1,success=1)
        return cls.unknown_error()
