from . import *
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

from .. import make_res, sanitize_input, Feed
from ..models import User
from ..models.Likes import Like


class Register(Resource):
    def post(self):
        j = request.json
        data = j.get('data')
        if not data:
            return make_res(msg='check input')
        data = sanitize_data(data)
        su = User.signup(data)
        p = j.get('platform')
        # if p:
        #     if 'andoid' == p:
        #         su['']
        return make_res(success=su.get('status'), res=su.get("res"), msg=su.get('msg'))


class Followers(Resource):
    @jwt_required()
    def post(self, process):
        j = request.json
        if hasattr(Follower, process):
            return getattr(Follower, process)()
        return make_res(msg="url endpoint not found")


class Followings(Resource):
    @jwt_required()
    def post(self, process):
        j = request.json
        if hasattr(Following, process):
            return getattr(Following, process)()
        return make_res(msg="url endpoint not found")


class Feeds(Resource):
    @jwt_required()
    def post(self, process):
        j = request.json
        if hasattr(Feed, process):
            return getattr(Feed, process)()
        return make_res(msg="url endpoint not found")

    @jwt_required()
    def get(self, process):
        if hasattr(Feed, process):
            return getattr(Feed, process)()
        return make_res(msg="url endpoint not found")


class Saved(Resource):
    def post(self):
        pass


class Collections(Resource):
    @jwt_required()
    def post(self, process):
        if hasattr(Collection, process):
            return getattr(Collection, process)()

        return getattr(Collection, "for_user")(process)


class Comments(Resource):
    @jwt_required()
    def post(self):
        j = request.json
        t = j.find('filters')
        pass

    @jwt_required()
    def get(self):
        j = request.json
        t = j.find('target')
        r = j.find('reply')

        return


class Likes(Resource):
    @jwt_required()
    def post(self, end):
        if hasattr(Like, end):
            return getattr(Like, end)()
        else:
            return getattr(Like, "count")(end)

    @jwt_required()
    def get(self, end):
        if hasattr(Like, end):
            return getattr(Like, end)()
        else:
            return getattr(Like, "count")(end)


class Update(Resource):
    def post(self):
        j = request.json
        d = j.get('data')
        if not d:
            return make_res(msg='check input')
        target = j.get('target')
        field = j.get('field')
        # print(j)
        if not field:
            return make_res(msg='specify the update field')
        if not target:
            return make_res(msg='specify the update target')
        for key, value in d.items():
            d[key] = encrypt_key(key, sanitize_input(value))
        up = User.update(get_table(field), target, d)


class Login(Resource):
    def post(self):
        j = request.json
        data = j.get('data')
        if not data:
            return make_res(msg='check input')
        ul = User.login(data)
        return make_res(success=ul['status'], msg=ul['msg'], res=ul.get('res'))


class UserEndpoint1(Resource):
    @jwt_required()
    def get(self, userend):
        if hasattr(UserEnd, userend):
            return getattr(UserEnd, userend)()
        return make_res(msg="url endpoint not found")

    def post(self, userend):
        if hasattr(UserEnd, userend):
            return getattr(UserEnd, userend)()
        return make_res(msg="url endpoint not found")


class UserEndpoint(Resource):
    def post(self):
        j = request.json
        f = j.get('filter')
        o = j.get('order')
        l = j.get('limit')
        action = j.get('action')
        if not action:
            return make_res(msg="Action required")
        sql = "select * from app_users"
        values = None
        if f:
            sql += ' where '
            values = []
            for key, value in f.items():
                sql += f" {key} = %s AND "
                values.append(value)
            sql = sql.rstrip(" AND ")
        if o:
            sql += ' order by '
            sql += ' rand() ' if o == 'random' else f' {o}'
        if l:
            sql += f' limit {l} '

        dt = DB.Read(sql, values)

        jsonStr = json.dumps(dt, indent=1, sort_keys=True, default=str)
        # then covert json string to json object
        return json.loads(jsonStr)

    def get(self):
        dt = DB.Read('select * from app_users')
        jsonStr = json.dumps(dt, indent=1, sort_keys=True, default=str)

        return json.loads(jsonStr)


class Messenger(Resource):
    def post(self, process):
        if hasattr(Messages, process):
            return getattr(Messages, process)()
        return make_res(msg="endpoint provided dont exixt")


class MC(Resource):
    def post(self):
        j = request.json
        data = j.get('data')
        if not data:
            return jsonify(msg="data required")
        _mc = User.mutual_connection(data)
        return make_res(success=1, res=_mc)
        sql = "select * from app_users"
        values = None
        if f:
            sql += ' where '
            values = []
            for key, value in f.items():
                sql += f" {key} = %s AND "
                values.append(value)
            sql = sql.rstrip(" AND ")
        if o:
            sql += ' order by '
            sql += ' rand() ' if o == 'random' else f' {o}'
        if l:
            sql += f' limit {l} '

        dt = DB.Read(sql, values)

        jsonStr = json.dumps(dt, indent=1, sort_keys=True, default=str)
        return json.loads(jsonStr)


class Member(Resource):
    """docstring for Member"""

    def post(self):
        j = request.json
        data = j.get('data')
        data = sanitize_data(data)
        if not data:
            return make_res(msg='check input')
        action = j.get('action')
        if not action:
            return make_res(msg='Action required. Please specify the operation to be handled')
        if hasattr(User, action):
            return make_res(success=1, msg=getattr(User, action)(data))
        else:
            return make_res(msg='Error. The action you are requesting is not working or does not exist')


class Files(Resource):
    def get(self, filename):
        return send_from_directory('static', filename)


class Auth(Resource):
    def post(self, process):
        if hasattr(AuthModel, process):
            return getattr(AuthModel, process)()
        return make_res(msg="access_denied")


class Notifications(Resource):
    @jwt_required()
    def post(self, process):
        if hasattr(Notes, process):
            return getattr(Notes, process)()
        return getattr(Notes, "get_notes")(process)


class Stars(Resource):
    @jwt_required()
    def post(cls, process):
        if hasattr(Star, process):
            return getattr(Star, process)()
        else:
            return make_res(msg="application Error")


class MSearch(Resource):
    def get(self, process):
        try:
            search = request.json.get("data").get("search") or None
            if hasattr(SearchModel, process):
                return getattr(SearchModel, process)(search)
            return make_res(msg="something went wrong")
        except Exception as e:
            return make_res(msg="application Error")
