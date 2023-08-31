import base64

from flask import request
from flask_jwt_extended import create_access_token, jwt_required

from . import *
from .. import gen_random, make_res, sanitize_input, sanitize_data, getNow
from datetime import *
from ...core.db import Connection
from ..resources.Image import FileProcessor


class User(Main):
    def __init__(self):
        super().__init__()

    @classmethod
    def data(cls, val, kw=None):
        d = val
        sql = f"select * from {cls.T_USERS} where "
        if kw:
            sql += f" {kw} = %s "
            return Connection().Read(sql, d)
        else:
            sql += " uname = %s or phone = %s or uid = %s"
            return Connection().Read(sql, [d, d, d])

    @classmethod
    def all_users(cls):
        sql = f"select * from {cls.T_USERS}"
        return DB.Read(sql)

    @classmethod
    def login(cls, data):
        phone = data.get('identity') or data.get('phone')
        password = data.get('password')

        if not phone or not password:
            return {'msg': 'check input', 'status': 0}

        password = sanitize_input(password)
        phone = sanitize_input(phone)

        d = cls.get_user_by_phone(data)

        if not d:
            return {'msg': f'Account{phone} is not found. Try other signin method or seek help.', 'status': 0}

        hashed_password = decrypt(d['password'])
        if hash_verify(password, hashed_password):
            d_upt = {
                'password': encrypt_key('password', password),
                'uid': d['uid']
            }
            access_token = create_access_token(identity=phone, fresh=True)
            refresh_token = create_refresh_token(phone)

            if cls.update(cls.T_USERS, d['uid'], d_upt):
                return {'res': {
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'info': d
                }, 'status': 1,
                    'msg': 'login success'}
        else:
            return {'msg': 'wrong password', 'status': 0}

    @classmethod
    def signup(cls, data):

        if cls.data(data["phone"], "phone"):
            return {'msg': 'action denied', 'status': 0}

        for key, value in data.items():
            data[key] = encrypt_key(key, sanitize_input(value))

        data['uid'] = gen_random(20)
        year = data.get('year')
        month = data.get('month')
        day = data.get('day')
        remove_keys(['day', 'month', 'year', 'username'], data)
        if day and month and year:
            data['dob'] = format_date(date(int(year), int(month), int(day)))
        data["active"] = 1
        data["status"] = "Just using hesa"
        data['joined'] = date.today()
        if cls.create(cls.T_USERS, data):
            access_token = create_access_token(identity=data['uid'], fresh=True)
            refresh_token = create_refresh_token(data['uid'])
            Config.set_theme(data['uid'], 1, True)
            return {
                'res': {
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'info': cls.data(data['uid'])
                },
                'msg': 'success',
                'status': 1
            }
        return {'msg': 'Failed. Try again', 'status': 0}

    @classmethod
    def exists(cls, kw):
        return True if cls.data(kw) else False

    @classmethod
    def is_member(cls, kw):
        res = 0
        if type(kw) == dict:
            res = {}
            for key, val in kw.items():
                res[key] = True if cls.data(val, key) else False
            return res

        return True if cls.data(kw) else False

    @classmethod
    def mutual_connection(cls, v):
        filters = v.get('filters')
        uid = v.get('uid') or v.get('identity')
        if not uid and not filters:
            return "user name, email or id is required"
        v = cls.data(uid or filters.get('uid'))
        v = {
            "uid": v['uid'],
            "user_gender": v['gender'],
            "name_pattern": v['uname'],
            "limit": 5,
        }
        # sql = f"SELECT {cls.T_USERS}.* FROM	{cls.T_USERS} WHERE	{cls.T_USERS}.uid != %s and {cls.T_USERS}.uid not in (select {cls.T_FOLLOW}.followingid from {cls.T_FOLLOW} where {cls.T_FOLLOW}.followerid = %s ) or {cls.T_USERS}.gender <> %s or app_users.uname LIKE %s	ORDER BY rand()	LIMIT %s"
        # d = [v['uid'], v['uid'], v['user_gender'], v['name_pattern'], v['limit']]
        sql = f"SELECT * from {cls.T_USERS} where uid != %s and uid not in (select followingid from {cls.T_FOLLOW} where followerid = %s )"
        return Connection().Read(sql, [v['uid'], v['uid']])

    @classmethod
    def get_user_by_phone(cls, data):
        sql = f"select * from {cls.T_USERS} where phone = %s"
        d = Connection().Read(sql, [data.get("phone") or data.get("identity")])
        return d


class UserEnd(User):
    @classmethod
    def all(cls):
        return make_res(res=cls.all_users(), success=1)

    @classmethod
    def new(cls):
        return

    @classmethod
    def info(cls):
        j = request.json.get("data")
        uid = j.get("user_id") or j.get("identity")
        if not uid:
            return make_res(msg="cannot fet data of null")
        u = cls.data(uid)
        return make_res(res=u, success=1 if u else 0)

    @classmethod
    def get_user_by_phone(cls):
        j = request.json.get("data")
        uid = j.get("phone") or j.get("identity")
        if not uid:
            return make_res(msg="cannot fet data of null")
        u = cls.data(uid, "phone")
        return make_res(res=u, success=1 if u else 0)

    @classmethod
    def friends(cls):
        j = request.json.get("data")
        uid = j.get("user_id") or j.get("identity")
        if not uid:
            return make_res(msg="cannot fet data of null")
        sql = f"select * from {cls.T_USERS} where uid != %s"
        u = Connection().Read(sql, uid)
        return make_res(res=u, success=1 if u else 0)

    @classmethod
    def verify_user_password(cls):
        d = request.json.get("data")
        if not d:
            return make_res(msg="")
        d = sanitize_data(d)
        password = d.get("password")
        if not password:
            return make_res(msg="Value Error:password")
        d = cls.data(d.get("user_id") or d.get("identity"))
        if not d:
            return make_res(msg="user error")
        hashed_password = decrypt(d['password'])
        if not hash_verify(password, hashed_password):
            return make_res(msg="User error")
        else:
            return make_res(success=1)

    @classmethod
    def modify(cls):
        data = request.json.get("data")
        if not data:
            return make_res(msg="")

        field = data.get("fields")
        if field:
            field = sanitize_data(field)
        kw = data.get("kw")
        key = data.get("key")
        command = data.get("command")
        if command and command == "password":
            return cls.__change_user_password(field, key, kw)

        d = cls.update(cls.T_USERS, key, field, kw)
        return make_res(success=1 if d else 0, res=True if d else False)

    @classmethod
    def modify_profile(cls):
        data = request.json.get("data")
        if not data:
            return cls.data_error()

        user = data.get("user_id") or data.get("identity") or None
        file = data.get("file") or None

        if not file:
            return make_res(msg="no files")

        print(file)

        file['content'] = base64.b64decode(file['content'])
        file = FileProcessor(file, "Avatar")

        data = {
            "profile": file.new_name
        }

        if cls.update(cls.T_USERS, user, data):
            file.upload("avatars")
            return make_res(success=1)
        return make_res(msg="error")

    @classmethod
    def __change_user_password(cls, fields, key, kw):
        old = fields.get("old")
        new = fields.get("new")
        if not old or not new:
            return cls.value_error()
        print("90")
        user = cls.t_data_or(cls.T_USERS, uid=key, uname=key)

        if not user:
            return make_res(msg="unable to change your password")
        p = decrypt(user['password'])

        if not hash_verify(old, p):
            return make_res(msg="wrong old password")
        new = encrypt(hash_password(new))
        if cls.update(cls.T_USERS, key, {"password": new}, kw):
            # if kw == "uid":
            #     data_notify = {
            #         'for_': key,
            #         'from_': key,
            #         'target': key,
            #         'type': 'security',
            #         'time': getNow(),
            #         'count': '0',
            #         'status': '0'
            #     }
            #     cls.create(cls.T_NOTE, data_notify)
            return make_res(success=1)
        return cls.unknown_error()


class Notes(Main):
    @classmethod
    @jwt_required()
    def get_notes(cls, user):
        sql = f"SELECT * FROM {cls.T_NOTE} WHERE for_ = %s ORDER BY time DESC"
        d = Connection().Read(sql, user)
        return make_res(res=d, success=1)
