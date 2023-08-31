from . import *
from . import Main
from .. import make_res


class Messages1(Main):
    @classmethod
    def new(cls):
        j = request.json.get("data")
        if not j:
            return make_res(msg="cant post empty data")

        sender = j.get("sender")
        receiver = j.get("receiver")
        message = j.get("message")
        data = {
            "msg": message,
            "msg_from": sender,
            "msg_to": receiver,
            "time": getNow()
        }
        sql_res = cls.create(cls.T_MESSAGES, data)
        if sql_res:
            return make_res(msg="success" if sql_res else "something went wrong", success=1 if sql_res else 0)


class Messages(Main):
    @classmethod
    def new(cls):
        j = request.json.get("data")
        if not j:
            return make_res(msg="cant post empty data")

        sender = j.get("sender")
        receiver = j.get("receiver")
        message = j.get("message")

        data = {
            "msg": message,
            "msg_from": sender,
            "msg_to": receiver,
            "time": getNow()
        }

        sql_res = cls.create(cls.T_MESSAGES, data)
        if sql_res:
            return make_res(msg="success" if sql_res else "something went wrong", success=1 if sql_res else 0)
        return make_res(msg="something went wrong")

    @classmethod
    def for_user(cls):
        data = request.json.get("data")
        if not data:
            return make_res(msg="data not found")

        me = data.get("sender")
        you = data.get("receiver")
        sql = (f"SELECT * from {cls.T_MESSAGES} where msg_from = %s "
               f"and msg_to = %s or msg_from =%s and msg_to = %s"
               f"  order by time asc")
        res = Connection().Read(sql, [me, you, you, me])
        if res:
            return make_res(res=res, success=1)

        return make_res(msg="nothing ")

    @classmethod
    def chat_list(cls):
        data = request.json.get("data")
        if not data:
            return make_res(msg="")
        uid = data.get("user_id") or data.get("identity")
        sql = (f"SELECT m.*, MAX(m.time) AS latest_message_date,COUNT(*) AS message_count,"
               f" (CASE WHEN m.msg_from = %s THEN m.msg_to  ELSE m.msg_from END) "
               f"AS chat_partner_id FROM {cls.T_MESSAGES} m WHERE m.msg_from = %s OR m.msg_to "
               f"= %s GROUP BY chat_partner_id ORDER BY  latest_message_date DESC")
        sql = Connection().Read(sql, [uid, uid, uid])

        return make_res(res=sql,success=1 if sql else 0)

